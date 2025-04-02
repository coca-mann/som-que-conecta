from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from backend.instruments.models import InstrumentBookings, UserInstrument, InstrumentTypes, InstrumentBrands
from backend.instruments.validators import validate_booking_conflict
from django.core.exceptions import ValidationError


class BookingValidatorTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester")
        self.brand = InstrumentBrands.objects.create(name="Yamaha")
        self.instrument_type = InstrumentTypes.objects.create(name="Violão")
        self.instrument = UserInstrument.objects.create(
            user_id=self.user,
            instrument_type_id=self.instrument_type,
            brand_id=self.brand,
            is_available=True
        )

    def test_conflicting_booking_raises_validation_error(self):
        InstrumentBookings.objects.create(
            instrument_id=self.instrument,
            user_id=self.user,
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2),
            status='CONFIRM'
        )

        conflicting_booking = InstrumentBookings(
            instrument_id=self.instrument,
            user_id=self.user,
            start_time=timezone.now() + timedelta(days=1, minutes=30),
            end_time=timezone.now() + timedelta(days=1, hours=3),
            status='PENDING'
        )

        with self.assertRaises(ValidationError):
            validate_booking_conflict(conflicting_booking)

    def test_non_conflicting_booking_passes(self):
        InstrumentBookings.objects.create(
            instrument_id=self.instrument,
            user_id=self.user,
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2),
            status='CONFIRM'
        )

        new_booking = InstrumentBookings(
            instrument_id=self.instrument,
            user_id=self.user,
            start_time=timezone.now() + timedelta(days=1, hours=3),
            end_time=timezone.now() + timedelta(days=1, hours=4),
            status='PENDING'
        )

        try:
            validate_booking_conflict(new_booking)
        except ValidationError:
            self.fail("validate_booking_conflict() levantou erro em uma reserva sem conflito.")
