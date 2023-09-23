from django.db import models
from django.utils import timezone

from apps.accounts.models import CustomUser


class ChatRoom(models.Model):
    participants = models.ManyToManyField(CustomUser, related_name='chatrooms')
    is_group = models.BooleanField(default=False)  # Это поле определяет, является ли чат групповым
    created_at = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=255, null=True, blank=True)  # Название для групповых чатов

    def __str__(self):
        if self.is_group:
            return self.room_name or f"Group chat of {self.participants.count()} members"
        return ', '.join([user.username for user in self.participants.all()])


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
