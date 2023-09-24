from django.contrib import messages
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Book
from ..userschats.models import Message
from ..activity.froms import ReviewForm
from ..activity.models import Review
from ..userschats.models import ChatRoom


@login_required
def share_book_in_chat(request):
    if request.method == "POST":
        book_id = request.POST.get('book_id')
        chat_ids = request.POST.getlist('chat_ids')
        book = get_object_or_404(Book, id=book_id)

        for chat_id in chat_ids:
            chatroom = get_object_or_404(ChatRoom, id=chat_id)
            # Создайте сообщение и отправьте книгу в выбранный чат
            # Здесь предполагается, что у вас есть модель Message с соответствующими полями
            Message.objects.create(chatroom=chatroom, sender=request.user,
                                   content=f"Посмотрите на эту книгу: {book.title}", book_shared=book)

        # Добавьте параметр в URL, чтобы указать успешное действие
        return redirect(f"{request.path_info}?success=true")


class BookListView(View):
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        chats = ChatRoom.objects.filter(participants=request.user)
        context = {
            'books': books,
            'chats': chats,
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

        existing_review = Review.objects.filter(user=request.user, book=book).first()

        if existing_review:
            messages.error(request, 'У вас уже есть рецензия на эту книгу. При желании, измените её.')
            return redirect('book_detail', book_id=book_id)

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


class ReviewUpdate(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'book/book_review_edit.html'

    def get_object(self, queryset=None):
        return Review.objects.filter(user=self.request.user, book_id=self.kwargs['book_id']).first()

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.book = get_object_or_404(Book, pk=self.kwargs['book_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'book_id': self.kwargs['book_id']})


class DeleteReviewView(DeleteView):
    model = Review

    def get_success_url(self):
        book_id = self.object.book.id
        messages.success(self.request, 'Рецензия успешно удалена.')
        return reverse_lazy('book_detail', kwargs={'book_id': book_id})


@login_required
def share_book_in_chat(request):
    if request.method == "POST":
        book_id = request.POST.get('book_id')
        chat_ids = request.POST.getlist('chat_ids')
        book = get_object_or_404(Book, id=book_id)

        for chat_id in chat_ids:
            chatroom = get_object_or_404(ChatRoom, id=chat_id)
            Message.objects.create(chatroom=chatroom, sender=request.user,
                                   content=f"Посмотрите на эту книгу: {book.title}", book_shared=book)

        return JsonResponse({"status": "success"})
