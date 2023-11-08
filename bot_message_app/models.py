from django.db import models
from django.db.models import JSONField


class MessageManager(models.Model):
    id = models.AutoField(primary_key=True)
    enabled = models.BooleanField(default=True, verbose_name='Enabled')
    name = models.CharField(max_length=150, verbose_name='Name')
    description = models.TextField(default='', blank=True, verbose_name='Description')
    add_param = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name


class MessengerType(models.Model):
    id = models.AutoField(primary_key=True)
    verbal = models.CharField(max_length=50, verbose_name='Verbal code')
    caption = models.CharField(max_length=50, verbose_name='Caption')

    def __str__(self):
        return self.caption


class Messenger(models.Model):
    id = models.AutoField(primary_key=True)
    messenger_type = models.ForeignKey(MessengerType, on_delete=models.PROTECT, related_name="messengers",
                                       verbose_name='Messenger type')
    verbal = models.CharField(max_length=50, verbose_name='Verbal code')
    caption = models.CharField(max_length=150, verbose_name='Caption')
    settings = models.JSONField(default=dict)

    def __str__(self):
        return self.caption
