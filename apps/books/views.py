from django.contrib import messages
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Book, Author, Genre
from ..userschats.models import Message
from ..activity.froms import ReviewForm
from ..activity.models import Review
from ..userschats.models import ChatRoom
from .forms import BookForm


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


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Замените 'book_list' на имя вашего представления для списка книг
    else:
        form = BookForm()

    return render(request, 'book/add_book.html', {'form': form})


def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')  # Замените 'book_list' на имя вашего представления для списка книг

    return render(request, 'book/delete_book.html', {'book': book})


def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Замените 'book_list' на имя вашего представления для списка книг
    else:
        form = BookForm(instance=book)

    return render(request, 'book/edit_book.html', {'form': form, 'book': book})

class AuthorCreateView(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'bio', 'birth_date', 'death_date']
    template_name = 'authors/add_authors.html'
    success_url = reverse_lazy('author_list')

    def form_valid(self, form):
        # Проверяем, существует ли автор с таким именем и фамилией
        existing_author = Author.objects.filter(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name']
        ).exists()

        if existing_author:
            messages.error(self.request, 'Автор с таким именем и фамилией уже существует')
            return self.form_invalid(form)

        return super().form_valid(form)


def author_list(request):
    authors = Author.objects.all()
    context = {
        'authors': authors
    }
    return render(request,'authors/author_list.html', context)

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'authors/author_detail.html'


class AuthorUpdateView(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'bio', 'birth_date', 'death_date']
    template_name = 'authors/author_edit.html'

    def get_initial(self):
        initial = super().get_initial()
        author = self.get_object()
        initial['first_name'] = author.first_name
        initial['last_name'] = author.last_name
        initial['bio'] = author.bio
        initial['birth_date'] = author.birth_date
        initial['death_date'] = author.death_date
        return initial

    def get_success_url(self):
        return reverse_lazy('author_detail', kwargs={'pk': self.object.pk})


class AuthorDeleteView(DeleteView):
    model = Author
    fields = '__all__'
    template_name = 'authors/author_delete.html'
    success_url = reverse_lazy('author_list')



class GenreCreateView(CreateView):
    model = Genre
    fields = '__all__'
    template_name = 'genres/genre_add.html'
    success_url = reverse_lazy('genre_list')

    def form_valid(self, form):

        existing_genre = Genre.objects.filter(
              name=form.cleaned_data['name'],

        ).exists()

        if existing_genre:
            messages.error(self.request, 'Жанр с таким названием уже существует')
            return self.form_invalid(form)

        return super().form_valid(form)


def genre_list(request):
    genres = Genre.objects.all()
    context = {
        'genres': genres
    }

    return render(request, 'genres/genre_list.html', context)


class GenreDetailView(DetailView):
    model = Genre
    template_name = 'genres/genre_detail.html'


class GenreUpdateView(UpdateView):
    model = Genre
    fields = '__all__'
    template_name = 'genres/genre_edit.html'

    def get_initial(self):
        initial = super().get_initial()
        genre = self.get_object()
        initial['name'] = genre.name
        initial['description'] = genre.description
        return initial

    def get_success_url(self):
        return reverse_lazy('genre_detail', kwargs={'pk': self.object.pk})


class GenreDeleteView(DeleteView):
    model = Genre
    fields = '__all__'
    template_name = 'genres/genre_delete.html'
    success_url = reverse_lazy('genre_list')
