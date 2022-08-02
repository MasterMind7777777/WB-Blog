from django.shortcuts import render
from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .paginators import SmallPageNumberPagination
from posts.models import Post
from posts.serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-id')
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    pagination_class = SmallPageNumberPagination
    serializer_class = PostSerializer
