from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.instruments.views import (
    InstrumentTypeViewSet,
    UserInstrumentViewSet,
    InstrumentBrandsViewSet,
    InstrumentBookingViewSet
)


router = DefaultRouter()
router.register('instrumenttype', InstrumentTypeViewSet)
router.register('userinstrument', UserInstrumentViewSet)
router.register('instrumentbrand', InstrumentBrandsViewSet)
router.register('instrumentbooking', InstrumentBookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
