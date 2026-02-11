from rest_framework import serializers
from ..Models.mission_model import MissionModel
from ..Models.vehicule_model import VehiculeModel
# config variables for computing mission id
PREFIX = "MSN"
TOTAL_LENGTH = 8

class MissionSerializer(serializers.ModelSerializer):
    mission_id = serializers.CharField(read_only=True, required=False)
    truck = serializers.PrimaryKeyRelatedField(
        queryset=VehiculeModel.objects.all(),
        write_only=True
    )
    truck_id = serializers.CharField(source="truck.license_plate", read_only=True)
    
    class Meta:
        model = MissionModel
        fields = "__all__"
        
    def create(self, validated_data):
        instance = super().create(validated_data)
        numeric_length = TOTAL_LENGTH - len(PREFIX)
        instance.mission_id = f"{PREFIX}{str(instance.pk).zfill(numeric_length)}"
        instance.save()
        return instance