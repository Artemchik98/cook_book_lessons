from rest_framework import viewsets
from .serializers import PostSerializer,PostPointSerializer
from ..models import Post,PostPoint

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostPointViewSet(viewsets.ModelViewSet):
    queryset = PostPoint.objects.all()
    serializer_class = PostPointSerializer