from rest_framework import serializers
from .models import Post
from users.serializers import UserSerializer
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


    def validate_name(self, name):
        if not name:
            raise serializers.ValidationError('Не заполнен Заголовок!')
        if self.context.get('request').method == 'POST':
            current_user = self.context.get('request').user
            if Post.objects.filter(author=current_user, name=name).exists():
                raise serializers.ValidationError(
                    'Пост с таким заголовоком у вас уже есть!'
                )
        return name

    def validate_text(self, text):
        if not text:
            raise serializers.ValidationError('Не заполнен тест поста!')
        return text

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance

    @transaction.atomic
    def create(self, validated_data):
        current_user = self.context.get('request').user
        name = self.validate_name(
            self.initial_data.get('name')
        )
        text = self.validate_text(
            self.initial_data.get('text')
        )
        post = Post.objects.create(
            author=current_user,
            name=name,
            text=text,
        )
        return post


class FollowerSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    posts = PostSerializer(many=True)
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_subscribed', 'posts', 'posts_count')

    @staticmethod
    def get_is_subscribed(obj):
        return True

    def get_posts_count(self, obj):
        return obj.posts.count()