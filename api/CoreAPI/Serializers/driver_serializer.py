from rest_framework import serializers
from ..Models.driver_model import DriverModel

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverModel
        fields = "__all__"