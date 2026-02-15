from rest_framework import serializers
from ..Models.article_model import ArticleModel
from ..Models.tag_model import TagModel

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
    

class ArticleTagSerializer(serializers.ModelSerializer):
    tag = serializers.CharField()
    class Meta:
        model = ArticleModel
        fields = ["tag"]  

    def update(self, instance, validated_data):
        code = validated_data.get("tag")
        try:
            tag = TagModel.objects.get_or_create(code = code)
            instance.tag.status = "ON"
            instance.tag.save()
        except Exception as e:
            raise serializers.ValidationError(e)
     
        return instance