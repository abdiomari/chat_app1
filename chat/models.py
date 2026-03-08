# chat/models.py
from django.db import models
from django.conf import settings


class Room(models.Model):
    name        = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    created_by  = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='created_rooms'
    )
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    room      = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    user      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    content   = models.TextField()
    edited    = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.user} in {self.room}: {self.content[:50]}'