from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .models import Book, Author, Genre
from ..activity.froms import ReviewForm
from ..activity.models import Review


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
        review_form = ReviewForm()
        review_list = Review.objects.filter(book=book)
        context = {
            'book': book,
            'review_form': review_form,
            'review_list': review_list
        }
        return render(request, 'book/book_detail.html', context=context)

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            user = request.user
            if user.is_authenticated:
                new_review = review_form.save(commit=False)
                new_review.user = user
                new_review.book = book
                new_review.save()
                messages.success(request, 'Рецензия успешно добавлена.')
            else:
                messages.error(request, 'Только зарегистрированные пользователи могут оставлять рецензии.')
        else:
            messages.error(request, 'Ошибка в заполнении формы рецензии.')

        return redirect('book_detail', book_id=book_id)