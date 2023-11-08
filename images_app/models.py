from django.db import models


class ImageFile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=256)
    content_type = models.CharField(max_length=256)
    size = models.IntegerField(default=0)


class Image(models.Model):
    origin = models.URLField(default='')
    thumb = models.URLField(default='')
