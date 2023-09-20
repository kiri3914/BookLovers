from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import Book, Author, Genre


class BookListView(View):
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        context = {
            'books': books
        }
        return render(request, 'book/book_list.html', context=context)


class BookDetailView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        context = {
            'book': book
        }
        return render(request, 'book/book_detail.html', context=context)
