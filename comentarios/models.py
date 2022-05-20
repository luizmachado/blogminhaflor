from django.db import models
from posts.models import Post
from django.contrib.auth.models import User
from django.utils import timezone


class Comment(models.Model):
    comment_name = models.CharField(max_length=150, verbose_name='Nome')
    comment_email = models.EmailField(verbose_name='Email')
    comment = models.TextField(verbose_name='Comentário')
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post')
    comment_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True,
                                     null=True, verbose_name='Autor')
    comment_date = models.DateTimeField(default=timezone.now, verbose_name='Data')
    comment_published = models.BooleanField(default=False, verbose_name='Publicado')

    def __str__(self):
        return self.comment_name
