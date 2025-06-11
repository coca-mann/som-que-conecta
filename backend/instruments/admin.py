from django.contrib import admin
from backend.instruments.models import InstrumentTypes

admin.site.register(InstrumentTypes)

class InstrumentTypesAdmin(admin.ModelAdmin):
    list_display = ('name',)
