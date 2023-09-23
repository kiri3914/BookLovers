from django.db import models
from django.db.models import Avg
from django.urls import reverse


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)

    @property
    def count_books(self):
        return self.author_books.all().count()

    def __str__(self):
        return self.first_name + " " + self.last_name


# Модель для жанра книги
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# Модель для книги
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ManyToManyField(Author, related_name='author_books')
    genre = models.ManyToManyField(Genre, related_name='genre_books')
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    description = models.TextField()

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'book_id': self.pk})

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        return self.book_reviews.aggregate(Avg('rating'))['rating__avg'] or 0.0
