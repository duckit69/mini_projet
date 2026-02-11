from django.contrib import admin

from .Models.article_model import ArticleModel
from .Models.driver_model import DriverModel
from .Models.tag_model import TagModel
from .Models.vehicule_model import VehiculeModel
from .Models.warehouse_model import WarehouseModel
from .Models.mission_model import MissionModel

# Register your models here.
admin.site.register(ArticleModel)
admin.site.register(DriverModel)
admin.site.register(TagModel)
admin.site.register(VehiculeModel)
admin.site.register(WarehouseModel)
admin.site.register(MissionModel)