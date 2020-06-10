from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.PoliceStationRecordKeeper)
admin.site.register(models.CourtRecordKeeper)
admin.site.register(models.DSPRecordKeeper)
admin.site.register(models.VRKRecordKeeper)
admin.site.register(models.SSPRecordKeeper)