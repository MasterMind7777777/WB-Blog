from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from api.paginators import SmallPageNumberPagination
from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from posts.serializers import CreateReadSerializer
from rest_framework import status
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-id')
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    pagination_class = SmallPageNumberPagination
    serializer_class = PostSerializer

    @action(detail=True, methods=['post'],
        permission_classes=[IsAuthenticated])
    def read(self, request, pk=None):
        serializer = CreateReadSerializer(
            data=dict(post=pk, user=request.user.id),
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)