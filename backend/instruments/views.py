from rest_framework import viewsets
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
    InstrumentBookingsSerializer
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


class UserInstrumentViewSet(viewsets.ModelViewSet):
    queryset = Instrument.objects.all()
    serializer_class = UserInstrumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Instrument.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)
