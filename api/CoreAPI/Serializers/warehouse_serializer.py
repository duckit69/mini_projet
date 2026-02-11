from rest_framework import serializers
from ..Models.warehouse_model import WarehouseModel

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseModel
        fields = "__all__"