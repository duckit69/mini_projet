from django.db import models

class DriverModel(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    license = models.CharField(max_length=9, null=False, blank=False)
    image = models.ImageField(upload_to='DriverImages/', default='default_driver.png'  , blank=True , null= True)
    
    def __str__(self):
        return str(self.name) + " " + str(self.license)