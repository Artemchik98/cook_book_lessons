from rest_framework import serializers
from ..models import Post,PostPoint

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostPointSerializer(serializers.ModelSerializer):
    class Meta:
        model= PostPoint
        fields='__all__'

