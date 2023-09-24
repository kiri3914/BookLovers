from django.db import models
from django.utils import timezone

from apps.accounts.models import CustomUser
from apps.books.models import Book


class ChatRoom(models.Model):
    participants = models.ManyToManyField(CustomUser, related_name='chatrooms')
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=255, null=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='created_chatrooms', null=True,
                               blank=True)


    def __str__(self):
        if self.is_group:
            return self.room_name or f"Group chat of {self.participants.count()} members"
        return ', '.join([user.username for user in self.participants.all()])

    def get_other_participant(self, user):
        return self.participants.exclude(id=user.id).first()


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    book_shared = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
