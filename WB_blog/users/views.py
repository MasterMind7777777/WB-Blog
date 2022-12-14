from .serializers import (CreateFollowSerializer, ShowFollowsSerializer,
                             UserSerializer)
from posts.serializers import FollowerSerializer           
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from .models import Follow
from posts.serializers import ShowPostSerializer
from posts.models import Post
from api.paginators import SmallPageNumberPagination
from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import operator

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    serializer_class = UserSerializer
    pagination_class = SmallPageNumberPagination

    def list(self, request, *args, **kwargs):
        response = super(CustomUserViewSet, self).list(request, args, kwargs)
        ordering = request.query_params.get('ordering')
        if ordering == None:
            ordering = '-id'
        response.data['results'] = sorted(response.data['results'], key=operator.itemgetter(ordering.replace('-',''),))

        if "-" in ordering:      
            response.data['results'] = sorted(response.data['results'], key=lambda k: (k[ordering.replace('-','')], ), reverse=True)
        else:
            response.data['results'] = sorted(response.data['results'], key=lambda k: (k[ordering], ))

        return response

    def get_queryset(self):
        return User.objects.all()

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        return super(CustomUserViewSet, self).me(request, *args, **kwargs)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ShowFollowsSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def subscriptions_posts(self, request):
        queryset = Post.objects.filter(author__following__user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ShowPostSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def posts(self, request, id=None):
        queryset = Post.objects.filter(author=id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ShowPostSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        serializer = CreateFollowSerializer(
            data=dict(author=id, user=request.user.id),
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        subscription = Follow.objects.filter(
            user=request.user,
            author=author
        )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'?????????????? ?????????????? ???????????????????????????? ????????????????!'},
            status=status.HTTP_400_BAD_REQUEST
        )


class FollowViewSet(ListAPIView):
    serializer_class = ShowFollowsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SmallPageNumberPagination

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)