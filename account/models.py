from django.db import models
from django.contrib import auth

# Create your models here.


class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return self.username


class PoliceStationRecordKeeper(models.Model):
    
    user = models.ForeignKey(auth.models.User, related_name='police_station_record_keepers', on_delete=models.CASCADE)
    police_station = models.ForeignKey("location.PoliceStation", related_name='police_station_record_keepers', on_delete=models.CASCADE)
    sub_division = models.ForeignKey("location.SubDivision", related_name='police_station_record_keepers', on_delete=models.CASCADE)


class CourtRecordKeeper(models.Model):
    
    user = models.ForeignKey(auth.models.User, related_name='court_record_keepers', on_delete=models.CASCADE)


class SSPRecordKeeper(models.Model):

    user = models.ForeignKey(auth.models.User, related_name='ssp_record_keepers', on_delete=models.CASCADE)