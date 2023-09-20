from django.db import models

from apps.accounts.models import CustomUser
from apps.books.models import Book


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_reviews')
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' ' + self.rating


class Activity(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.review
