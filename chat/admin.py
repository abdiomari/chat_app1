from django.contrib import admin

# Register your models here.
from .models import Room, Message


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'content', 'timestamp']
    list_filter = ['room']
    search_fields = ['content', 'user__username']