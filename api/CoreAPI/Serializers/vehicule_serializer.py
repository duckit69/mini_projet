from rest_framework import serializers
from ..Models.vehicule_model import VehiculeModel

# config variables for computing mission id
PREFIX_MODEL = "MR"
TOTAL_LENGTH_MODEL = 4
PREFIX_PLATE = "TRK"
TOTAL_LENGTH_PLATE = 8

class VehiculeSerializer(serializers.ModelSerializer):
    model = serializers.CharField(read_only=True, required=False)
    license_plate = serializers.CharField(read_only=True, required=False)
    class Meta:
        model = VehiculeModel
        fields = "__all__"
    
    def create(self, validated_data):
        print(validated_data)
        instance = super().create(validated_data)
        # MODEL
        numeric_length = TOTAL_LENGTH_MODEL - len(PREFIX_MODEL)
        instance.model = f"{PREFIX_MODEL}{str(instance.pk).zfill(numeric_length)}"
        
        # LICENSE PLATE
        numeric_length = TOTAL_LENGTH_PLATE - len(PREFIX_PLATE)
        instance.license_plate = f"{PREFIX_PLATE}{str(instance.pk).zfill(numeric_length)}"
        instance.save()
        return instance