from rest_framework import serializers
from backend.instruments.models import (
    InstrumentBookings,
    InstrumentBrands,
    InstrumentTypes,
    Instrument
)


class InstrumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentTypes
        fields = '__all__'


class InstrumentBrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentBrands
        fields = '__all__'


class InstrumentBookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstrumentBookings
        fields = '__all__'


class UserInstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = '__all__'
