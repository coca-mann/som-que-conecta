from rest_framework import viewsets, generics, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from django.db import transaction
from .models import (
    InstrumentTypes,
    InstrumentBrands,
    InstrumentBookings,
    Instrument,
    InstrumentPictures
)
from backend.instruments.serializers import (
    InstrumentTypeSerializer,
    UserInstrumentSerializer,
    InstrumentBrandsSerializer,
    InstrumentSerializer,
    InstrumentBookingCreateSerializer,
    InstrumentBookingDetailSerializer,
    InstrumentBookingUpdateSerializer
)
from backend.instruments.permissions import CanUpdateBookingStatus
import json


class InstrumentTypeViewSet(viewsets.ModelViewSet):
    queryset = InstrumentTypes.objects.all()
    serializer_class = InstrumentTypeSerializer
    permission_classes = [IsAuthenticated]


class InstrumentBrandsViewSet(viewsets.ModelViewSet):
    queryset = InstrumentBrands.objects.all()
    serializer_class = InstrumentBrandsSerializer


class InstrumentBookingViewSet(mixins.CreateModelMixin,      # Para POST (create)
                               mixins.RetrieveModelMixin,   # Para GET de um item (retrieve)
                               mixins.UpdateModelMixin,     # Para PUT e PATCH (update)
                               mixins.ListModelMixin,       # Para GET de lista (list)
                               viewsets.GenericViewSet):    # Base para combinar os mixins
    """
    ViewSet para Agendamentos de Instrumentos.
    - Permite: Criar, Listar, Ver Detalhes e Atualizar.
    - Não Permite: Excluir.
    """
    queryset = InstrumentBookings.objects.all().order_by('-reservation_date')

    def get_serializer_class(self):
        """ Retorna o serializer apropriado com base na ação. """
        if self.action in ['update', 'partial_update']:
            return InstrumentBookingUpdateSerializer
        if self.action == 'create':
            return InstrumentBookingCreateSerializer
        return InstrumentBookingDetailSerializer

    def get_permissions(self):
        """
        Retorna as permissões apropriadas com base na ação.
        - Para criar, basta estar autenticado.
        - Para atualizar, precisa ser o dono do instrumento ou quem agendou.
        """
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), CanUpdateBookingStatus()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Filtra os agendamentos para que os usuários vejam apenas o que lhes diz respeito.
        - Alunos veem seus próprios agendamentos.
        - Professores/ONGs veem os agendamentos de seus instrumentos.
        """
        user = self.request.user
        # Filtra por agendamentos feitos pelo usuário
        bookings_by_user = InstrumentBookings.objects.filter(user_id=user)
        # Filtra por agendamentos dos instrumentos que pertencem ao usuário
        bookings_for_user_instruments = InstrumentBookings.objects.filter(instrument_id__user_id=user)
        
        # Combina os dois querysets sem duplicatas
        return (bookings_by_user | bookings_for_user_instruments).distinct().select_related(
            'instrument_id', 'user_id'
        )


class UserInstrumentListView(generics.ListAPIView):
    """ Utilizado nas URLs de Accounts para mostrar instrumentos na pagina de perfil do usuário """
    serializer_class = UserInstrumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filtra os instrumentos pelo usuário e otimiza a consulta para
        incluir os dados relacionados (marca, tipo e fotos).
        """
        user = self.request.user
        
        return Instrument.objects.filter(
            user_id=user  # Usa 'user_id' conforme seu modelo
        ).select_related(
            'brand', 'type'  # Otimiza a busca dos nomes da marca e tipo
        ).prefetch_related(
            'instrumentpictures_set'  # Pré-busca todas as fotos de uma vez
        )


class InstrumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar (CRUD) os Instrumentos do usuário.
    """
    serializer_class = InstrumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_parser_classes(self):
        """
        Seleciona o parser correto com base na ação.
        """
        # Para a nossa ação de upload de arquivos, usamos o MultiPartParser.
        if self.action == 'update_with_files':
            return [MultiPartParser(), FormParser()]
        
        # Para todas as outras ações (GET, DELETE, PATCH de JSON),
        # usamos os parsers padrão do DRF.
        return api_settings.DEFAULT_PARSER_CLASSES

    def get_queryset(self):
        """
        Retorna uma lista otimizada de instrumentos para o usuário autenticado.
        """
        return Instrument.objects.filter(user_id=self.request.user).select_related(
            'brand', 'type'
        ).prefetch_related(
            'instrumentpictures_set', 'instrumentbookings_set'
        )

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Cria um novo instrumento, manipulando os nomes de marca/tipo e as imagens.
        """
        data = request.POST.copy()

        # 1. Busca os objetos Brand e Type a partir dos nomes
        brand_name = data.get('brand_name')
        type_name = data.get('type_name')
        if not brand_name or not type_name:
            return Response({"error": "brand_name and type_name are required."}, status=status.HTTP_400_BAD_REQUEST)

        brand, _ = InstrumentBrands.objects.get_or_create(name=brand_name)
        try:
            instrument_type = InstrumentTypes.objects.get(name=type_name)
        except InstrumentTypes.DoesNotExist:
            return Response({"error": f"Type '{type_name}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Prepara os dados para o serializer
        data['brand'] = brand.id
        data['type'] = instrument_type.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # 3. Salva a instância principal do instrumento
        instrument = serializer.save(user_id=self.request.user)

        # 4. Salva as imagens associadas
        pictures = request.FILES.getlist('new_pictures')
        for picture in pictures:
            InstrumentPictures.objects.create(instrument_id=instrument, picture=picture)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    @action(detail=True, methods=['post'])
    @transaction.atomic
    def update_with_files(self, request, pk=None):
        """
        Ação customizada que usa POST para atualizar um instrumento,
        tratando corretamente multipart/form-data.
        """
        instrument = self.get_object()
        serializer = self.get_serializer(instance=instrument, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Lógica de atualização de Marca e Tipo
        brand_name = request.data.get('brand_name')
        if brand_name:
            brand, _ = InstrumentBrands.objects.get_or_create(name=brand_name)
            instrument.brand = brand

        type_name = request.data.get('type_name')
        if type_name:
            if type_obj := InstrumentTypes.objects.filter(name=type_name).first():
                instrument.type = type_obj
        
        instrument = serializer.save()

        # Adiciona novas imagens
        pictures = request.FILES.getlist('new_pictures')
        for picture in pictures:
            InstrumentPictures.objects.create(instrument_id=instrument, picture=picture)

        # Deleta imagens marcadas (COM A CHAVE CORRIGIDA)
        ids_to_delete_str = request.data.get('images_to_delete', '[]')
        ids_to_delete = json.loads(ids_to_delete_str)
        if ids_to_delete:
            InstrumentPictures.objects.filter(
                id__in=ids_to_delete,
                instrument_id=instrument.id
            ).delete()
        
        final_serializer = self.get_serializer(instrument)
        return Response(final_serializer.data)
    

class InstrumentPublicListView(generics.ListAPIView):
    """
    View para listar todos os instrumentos ATIVOS para qualquer usuário logado.
    """
    # Use o seu serializer existente que já atende aos requisitos.
    serializer_class = InstrumentSerializer # <--- A ÚNICA MUDANÇA É AQUI
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retorna apenas instrumentos com is_active=True.
        Otimiza a query usando select_related e prefetch_related.
        """
        return Instrument.objects.filter(is_active=True).select_related(
            'type', 'brand', 'user_id'
        ).prefetch_related(
            'instrumentpictures_set' # Necessário para o get_main_image funcionar eficientemente
        )