from django.contrib import admin

from .models import MessageManager, MessengerType, Messenger


@admin.register(MessageManager)
class MessageManagerAdmin(admin.ModelAdmin):
    list_display = ('id', 'enabled', 'name', 'add_param', 'description')
    search_fields = ('name',)


@admin.register(MessengerType)
class MessengerTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'verbal', 'caption')


@admin.register(Messenger)
class MessengerAdmin(admin.ModelAdmin):
    list_display = ('id', 'messenger_type', 'verbal', 'caption', 'settings')
