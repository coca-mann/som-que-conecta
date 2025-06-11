from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
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
    InstrumentBookingsSerializer,
    InstrumentSerializer
)


class InstrumentTypeViewSet(viewsets.ModelViewSet):
    queryset = InstrumentTypes.objects.all()
    serializer_class = InstrumentTypeSerializer
    permission_classes = [IsAuthenticated]


class InstrumentBrandsViewSet(viewsets.ModelViewSet):
    queryset = InstrumentBrands.objects.all()
    serializer_class = InstrumentBrandsSerializer


class InstrumentBookingViewSet(viewsets.ModelViewSet):
    queryset = InstrumentBookings.objects.all()
    serializer_class = InstrumentBookingsSerializer


class UserInstrumentListView(generics.ListAPIView):
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
    parser_classes = [MultiPartParser, FormParser]


    def get_queryset(self):
        """
        Esta view deve retornar uma lista de todos os instrumentos
        para o usuário atualmente autenticado.
        """
        return Instrument.objects.filter(user_id=self.request.user).select_related('brand', 'type').prefetch_related('instrumentpictures_set', 'instrumentbookings_set')

    @transaction.atomic # Garante que todas as operações no banco de dados sejam um sucesso ou falhem juntas
    def perform_create(self, serializer):
        # Primeiro, salva o instrumento para obter um ID
        instrument = serializer.save(user_id=self.request.user)

        # Agora, lida com as novas fotos
        pictures = self.request.FILES.getlist('pictures')
        for picture in pictures:
            InstrumentPictures.objects.create(instrument_id=instrument, picture=picture)

    @transaction.atomic
    def perform_update(self, serializer):
        # Pega a instância do instrumento que está sendo atualizada
        instrument = self.get_object()

        # Pega os nomes da marca e do tipo do request
        brand_name = self.request.data.get('brand_name')
        type_name = self.request.data.get('type_name')

        # Se o nome da marca foi enviado, busca ou cria a marca e pega o ID
        if brand_name:
            brand, _ = InstrumentBrands.objects.get_or_create(name=brand_name)
            instrument.brand = brand

        # Se o nome do tipo foi enviado, busca o tipo correspondente e pega o ID
        if type_name:
            try:
                instrument_type = InstrumentTypes.objects.get(name=type_name)
                instrument.type = instrument_type
            except InstrumentTypes.DoesNotExist:
                # Lide com o caso de um tipo não existente, se necessário
                # Por exemplo, levantando um erro de validação.
                pass
                
        # Salva o objeto Instrument com as ForeignKeys atualizadas
        instrument.save()
        
        # Agora, passa a instância atualizada para o serializer salvar os outros campos
        serializer.save()

        # O resto da lógica para lidar com imagens continua a mesma
        pictures = self.request.FILES.getlist('images') # Alterei para 'images' para bater com o frontend
        for picture in pictures:
            InstrumentPictures.objects.create(instrument_id=instrument, picture=picture)
        
        import json
        ids_to_delete_str = self.request.data.get('images_to_delete', '[]')
        ids_to_delete = json.loads(ids_to_delete_str)

        if ids_to_delete:
            InstrumentPictures.objects.filter(id__in=ids_to_delete).delete()

