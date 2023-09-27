from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from .views import AuthorUpdateView, AuthorDeleteView

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('detail/<int:book_id>', views.BookDetailView.as_view(), name='book_detail'),
    path('book/<int:book_id>/review/', views.ReviewUpdate.as_view(), name='edit_review'),
    path('book/<int:book_id>/review/<int:pk>/delete/', views.DeleteReviewView.as_view(), name='delete_review'),
    path('share_book_in_chat/', views.share_book_in_chat, name='share_book_in_chat'),
    path('add_book/', views.add_book, name='add_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('author/add/',views.AuthorCreateView.as_view(), name='add_author'),
    path('authors', views.author_list, name='author_list'),
    path('author_detail/<int:pk>/',views.AuthorDetailView.as_view(), name='author_detail'),
    path('author/<int:pk>/edit/', AuthorUpdateView.as_view(), name='author_edit'),
    path('author/<int:pk>/delete/',AuthorDeleteView.as_view(), name='author_delete'),
    path('genre/add/', views.GenreCreateView.as_view(), name='genre_add'),
    path('genres', views.genre_list, name='genre_list'),
    path('genre_detail/<int:pk>',views.GenreDetailView.as_view(), name='genre_detail'),
    path('genre/<int:pk>/edit/', views.GenreUpdateView.as_view(), name='genre_edit'),
    path('genre/<int:pk>/delete/',views.GenreDeleteView.as_view(), name='genre_delete'),

    ]

