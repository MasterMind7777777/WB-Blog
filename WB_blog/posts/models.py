from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Post(models.Model):
    """Модель статьи в блоге."""
    name = models.CharField()
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    def __str__(self):
        return self.name[:15]

    class Meta:
        ordering = ['-pub_date']
