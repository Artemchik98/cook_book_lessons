
from rest_framework import viewsets, status

from .serializers import CommentSerializer
from .serializers import PostSerializer, PostPointSerializer
from ..models import Comment
from ..models import Post, PostPoint


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostPointViewSet(viewsets.ModelViewSet):
    queryset = PostPoint.objects.all()
    serializer_class = PostPointSerializer


from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def post_list(request):
    objects = Post.objects.all()
    serializer_class = PostSerializer(objects, many=True)
    return Response(serializer_class.data)


@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    post_serializer = PostSerializer(post)
    post_points = PostPoint.objects.filter(post=post)
    post_points_serializer = PostPointSerializer(post_points, many=True)
    comments = Comment.objects.filter(post=post)
    comments_serializer = CommentSerializer(comments, many=True)
    return Response({'post': post_serializer.data,
                     'post_points': post_points_serializer.data,
                     'comments': comments_serializer.data})


@api_view(['POST'])
def post_create(request):
    serializer=PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def post_point_create(request):
    serializer=PostPointSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['PUT'])
def comment_create(request):
    serializer=CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['PUT'])
def post_update(request,pk):
    post = Post.objects.get(id=pk)
    serializer=PostSerializer(data=request.data,instance=post)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['PUT'])
def post_point_update(request,pk):
    post_point = PostPoint.objects.get(id=pk)
    serializer=PostPointSerializer(data=request.data,instance=post_point)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['PUT'])
def comment_update(request,pk):
    comment=Comment.objects.get(id=pk)
    serializer=CommentSerializer(data=request.data,instance=comment)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


from django.http import JsonResponse
@api_view(['DELETE'])
def post_delete(request,pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return  JsonResponse({'deleted, status':status.HTTP_204_NO_CONTENT})

@api_view(['DELETE'])
def post_point_delete(request,pk):
    post_point = PostPoint.objects.get(id=pk)
    post_point.delete()
    return  JsonResponse({'deleted, status':status.HTTP_204_NO_CONTENT})

@api_view(['DELETE'])
def comment_delete(request,pk):
    comment=Comment.objects.get(id=pk)
    comment.delete()
    return  JsonResponse({'deleted, status':status.HTTP_204_NO_CONTENT})
