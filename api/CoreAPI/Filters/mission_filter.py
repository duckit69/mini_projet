# filters.py
import django_filters
from ..Models.mission_model import MissionModel

class MissionFilter(django_filters.FilterSet):
    status = django_filters.MultipleChoiceFilter(
        field_name='status',
        choices=MissionModel.STATUS_CHOICES,
    )

    class Meta:
        model = MissionModel
        fields = "__all__"  