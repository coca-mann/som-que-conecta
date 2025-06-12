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
router.register('instrumentbooking', InstrumentBookingViewSet)
router.register('instruments', InstrumentViewSet, basename='instruments')
router.register('instruments-public-list', InstrumentPublicListView, basename='instruments-public')

urlpatterns = [
    path('', include(router.urls)),
]
