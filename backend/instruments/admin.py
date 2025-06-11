from django.contrib import admin
from backend.instruments.models import (
    InstrumentTypes,
    Instrument,
    InstrumentBookings,
    InstrumentBrands,
    InstrumentPictures)

admin.site.register(InstrumentTypes)
admin.site.register(Instrument)
admin.site.register(InstrumentBookings)
admin.site.register(InstrumentBrands)
admin.site.register(InstrumentPictures)


class InstrumentTypesAdmin(admin.ModelAdmin):
    list_display = ('name',)


class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('name',)


class InstrumentBookingsAdmin(admin.ModelAdmin):
    list_display = ('name',)


class InstrumentBrandsAdmin(admin.ModelAdmin):
    list_display = ('name',)


class InstrumentPicturesAdmin(admin.ModelAdmin):
    list_display = ('name',)
