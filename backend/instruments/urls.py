from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.instruments.views import (
    InstrumentTypeViewSet,
    InstrumentBrandsViewSet,
    InstrumentBookingViewSet,
    InstrumentViewSet,
    InstrumentPublicListView
)


router = DefaultRouter()
router.register('instrumenttype', InstrumentTypeViewSet)
router.register('instrumentbrand', InstrumentBrandsViewSet)
router.register(r'bookings', InstrumentBookingViewSet, basename='instrument-booking')
router.register('instruments', InstrumentViewSet, basename='instruments')

urlpatterns = [
    path('', include(router.urls)),
    path('instruments-public-list/', InstrumentPublicListView.as_view(), name='instruments-public')
]
