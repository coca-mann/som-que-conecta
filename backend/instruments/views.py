from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import (
    InstrumentTypes,
    InstrumentBrands,
    InstrumentBookings,
    Instrument
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

    def get_queryset(self):
        """
        Esta view deve retornar uma lista de todos os instrumentos
        para o usuário atualmente autenticado.
        """
        return Instrument.objects.filter(user_id=self.request.user).select_related('brand', 'type').prefetch_related('instrumentpictures_set', 'instrumentbookings_set')

    def perform_create(self, serializer):
        """
        Associa o instrumento ao usuário logado ao salvar.
        """
        serializer.save(user_id=self.request.user)

