from rest_framework import serializers
from backend.instruments.models import (
    InstrumentAvailability,
    InstrumentBookings,
    InstrumentBrands,
    InstrumentTypes,
    UserInstrument
)


class InstrumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentTypes
        fields = '__all__'


class InstrumentBrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentBrands
        fields = '__all__'


class InstrumentAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentAvailability
        fields = '__all__'


class InstrumentBookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentBookings
        fields = '__all__'


class UserInstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInstrument
        fields = '__all__'
