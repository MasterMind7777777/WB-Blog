from rest_framework import serializers
from .models import Post
from users.models import Read
from users.serializers import UserSerializer
from django.db import transaction
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    is_readed = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_is_readed(self, post):
        user = self.context.get('request').user
        return not user.is_anonymous and Read.objects.filter(
            user=user,
            post=post.id
        ).exists()

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

class ShowPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'

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


class CreateReadSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    post = serializers.IntegerField(source='post.id')

    class Meta:
        model = Read
        fields = ['user', 'post']

    def validate(self, data):
        user = data['user']['id']
        post = data['post']['id']
        read_exist = Read.objects.filter(
            user__id=user, post__id=post
        ).exists()
        if read_exist:
            raise serializers.ValidationError({"errors": 'Вы уже пометили как проитаныый'})
        return data

    def create(self, validated_data):
        post = validated_data.get('post')
        post = get_object_or_404(Post, pk=post.get('id'))
        user = User.objects.get(id=validated_data["user"]["id"])
        Read.objects.create(user=user, post=post)
        return validated_data