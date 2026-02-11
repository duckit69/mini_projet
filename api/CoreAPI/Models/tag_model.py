from django.db import models

class TagModel(models.Model):
    
    TAG_STATUS_CHOICES = [
        ('ON', 'in use'),
        ('OFF', 'standby'),
    ]
    
    code = models.CharField(max_length=20, blank=False, null=False, unique=True)
    status = models.CharField(max_length=10, choices=TAG_STATUS_CHOICES, default='OFF')
    
    def __str__(self):
        return str(self.code) + " " + str(self.status)