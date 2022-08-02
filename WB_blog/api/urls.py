from django.urls import include, path
from .views import PostViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
]