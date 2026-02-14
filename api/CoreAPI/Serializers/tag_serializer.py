from rest_framework import serializers
from ..Models.tag_model import TagModel

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = "__all__"