from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .tag_model import TagModel

class ArticleModel(models.Model):
    content = models.CharField(max_length=150, null=False, blank=False)
    source = models.CharField(max_length=100, null=False, blank=False)
    destination = models.CharField(max_length=100, null=False, blank=False)
    tag = models.ForeignKey(to=TagModel, on_delete=models.PROTECT, null=False)
    
    site_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=models.Q(
            app_label="CoreAPI",
            model__in=["vehiculemodel", "warehousemodel"]
        )
    )
    site_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('site_type', 'site_id')
    
    def __str__(self):
        return str(self.content) + " " + str(self.source) + " -> " + str(self.destination)
