from django.db import models
from categorias.models import Category
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from PIL import Image
from pathlib import Path


class Post(models.Model):
    post_title = models.CharField(max_length=255, verbose_name='Título')
    post_author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Autor')
    post_date = models.DateTimeField(default=timezone.now, verbose_name='Data')
    post_content = models.TextField(verbose_name='Conteúdo')
    post_brief = models.TextField(verbose_name='Síntese')
    post_category = models.ForeignKey(Category, on_delete=models.DO_NOTHING,
                                      blank=True, null=True, verbose_name='Categoria')
    post_image = models.ImageField(upload_to='post_img/%Y/%m/%d',
                                   blank=True, null=True, verbose_name='Imagem')
    post_published = models.BooleanField(default=False, verbose_name='Publicado')


    def __str__(self):
        return self.post_title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.resize_image(self.post_image.name, 800)


    @staticmethod
    def resize_image(image_name, new_width):
        image_path = Path(settings.MEDIA_ROOT / image_name)
        img = Image.open(image_path)
        width, height = img.size
        if width <= 800:
            img.close()
            return
        new_height = round((height * new_width) / width)
        new_img = img.resize((new_width, new_height), Image.ANTIALIAS)
        new_img.save(
            image_path,
            optimize=True,
            quality=60,
        )
        img.close()
        new_img.close()
