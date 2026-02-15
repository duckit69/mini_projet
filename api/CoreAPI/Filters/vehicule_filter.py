# filters.py
import django_filters
from ..Models.vehicule_model import VehiculeModel

class VehiculeFilter(django_filters.FilterSet):
    class Meta:
        model = VehiculeModel
        fields = ["available"]  