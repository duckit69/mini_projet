from django.db import models
from .article_model import ArticleModel

class VehiculeModel(models.Model):
    model = models.CharField(max_length=100, blank=False, null=False)
    license_plate = models.CharField(max_length=12, blank=False, null=False)
    
    AVAILABILITY_CHOICES = [
        ('Free', 'Free'),
        ('Used', 'Used'),
    ]
    available = models.CharField(max_length=5, choices=AVAILABILITY_CHOICES, default='Free', null=False, blank=False)
    # articles = models.Many
    
    def __str__(self):
        return str(self.model) + " " + str(self.license_plate)