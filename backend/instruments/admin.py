from django.contrib import admin
from .models import InstrumentBrands, InstrumentTypes, UserInstrument

admin.site.register(InstrumentBrands)
admin.site.register(InstrumentTypes)

@admin.register(UserInstrument)
class UserInstrumentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'instrument_type_id', 'color', 'brand_id', 'is_available', 'location')
    list_filter = ('brand_id', 'instrument_type_id', 'color')
    search_fields = ('user_id__username', 'instrument_type_id__name', 'brand_id__name')

    fieldsets = (
        ('Informações do Instrumento', {
            'fields': ('user_id', 'instrument_type_id', 'brand_id', 'color', 'description', 'location', 'is_available'),
        }),
        ('Datas', {
            'fields': ('created_at', 'modified_at'),
        }),
    )
    readonly_fields = ('created_at', 'modified_at')