from rest_framework import serializers
from ..Models.article_model import ArticleModel

# config variables for computing content
PREFIX = "AR"
TOTAL_LENGTH = 4

class ArticleSerializer(serializers.ModelSerializer):
    content = serializers.CharField(read_only=True, required=False)
    
    class Meta:
        model = ArticleModel
        fields = "__all__"
        
    def create(self, validated_data):
        instance = super().create(validated_data)
        numeric_length = TOTAL_LENGTH - len(PREFIX)
        instance.content = f"{PREFIX}{str(instance.pk).zfill(numeric_length)}"
        instance.save()
        return instance