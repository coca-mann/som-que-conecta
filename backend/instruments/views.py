from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import (
    InstrumentTypes,
    InstrumentBrands,
    InstrumentAvailability,
    InstrumentBookings,
    UserInstrument
)
from backend.instruments.serializers import (
    InstrumentTypeSerializer,
    UserInstrumentSerializer,
    InstrumentBrandsSerializer,
    InstrumentBookingsSerializer,
    InstrumentAvailabilitySerializer
)


class InstrumentTypeViewSet(viewsets.ModelViewSet):
    queryset = InstrumentTypes.objects.all()
    serializer_class = InstrumentTypeSerializer
    permission_classes = [IsAuthenticated]


class InstrumentBrandsViewSet(viewsets.ModelViewSet):
    queryset = InstrumentBrands.objects.all()
    serializer_class = InstrumentBrandsSerializer


class InstrumentAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = InstrumentAvailability.objects.all()
    serializer_class = InstrumentAvailabilitySerializer


class InstrumentBookingViewSet(viewsets.ModelViewSet):
    queryset = InstrumentBookings.objects.all()
    serializer_class = InstrumentBookingsSerializer


class UserInstrumentViewSet(viewsets.ModelViewSet):
    queryset = UserInstrument.objects.all()
    serializer_class = UserInstrumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserInstrument.objects.filter(user_id=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)