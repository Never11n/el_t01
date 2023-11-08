from django.db import models


class AttachmentFile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=256)
    system_name = models.CharField(max_length=256)
    content_type = models.CharField(max_length=256)
    size = models.IntegerField(default=0)
    extension = models.CharField(default='', max_length=50)
