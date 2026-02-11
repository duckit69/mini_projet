from django.db import models
from .vehicule_model import VehiculeModel


class MissionModel(models.Model):
    mission_id = models.CharField(max_length=8, blank=False, null=False)
    truck = models.ForeignKey(to=VehiculeModel, on_delete=models.PROTECT, blank=False, null=False)
    source = models.CharField(max_length=20, blank=False, null=False)
    destination = models.CharField(max_length=20, blank=False, null=False)
    
    STATUS_CHOICES = [
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    
    def __str__(self):
        return str(self.mission_id) +"_"+ str(self.truck_id) +" : "+ str(self.source) +" -> "+ str(self.destination)