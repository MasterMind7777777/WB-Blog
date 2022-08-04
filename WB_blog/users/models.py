from django.contrib.auth import get_user_model
from django.db import models
from posts.models import Post

User = get_user_model()


class Follow(models.Model):
    """Модель подписки на автора."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique follow')
        ]

class Read(models.Model):
    """Модель чтоб отметить что пост прочитан пользователем."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reader')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='readed')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'], name='unique read')
        ]

