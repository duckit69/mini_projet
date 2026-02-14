from django.db import models

class WarehouseModel(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    address = models.CharField(max_length=200, blank=False, null=False)
    
    def __str__(self):
        return str(self.name) + " " + str(self.address)