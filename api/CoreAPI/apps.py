from django.apps import AppConfig


class CoreapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CoreAPI'
    label = 'CoreAPI'
    
    def ready(self):
        from .Models.vehicule_model import VehiculeModel
        from .Models.warehouse_model import WarehouseModel
