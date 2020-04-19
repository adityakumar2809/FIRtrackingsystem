from django.db import models

# Create your models here.


class SubDivision(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class PoliceStation(models.Model):
    sub_division = models.ForeignKey("location.SubDivision", related_name='police_stations',on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    