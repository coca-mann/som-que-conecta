from django.db import models
from django.contrib.auth.models import User

class InstrumentBrands(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class InstrumentTypes(models.Model):
    name = models.CharField(null=False, blank=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class UserInstrument(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    instrument_type_id = models.ForeignKey(InstrumentTypes, on_delete=models.PROTECT)
    color = models.CharField(max_length=50, blank=True, null=True)
    brand_id = models.ForeignKey(InstrumentBrands, on_delete=models.PROTECT, null=False)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.instrument_type_id.name} {self.color}"