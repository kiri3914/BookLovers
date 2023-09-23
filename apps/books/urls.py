from django.urls import path
from . import views


urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('detail/<int:book_id>', views.BookDetailView.as_view(), name='book_detail'),
    path('book/<int:book_id>/review/', views.ReviewUpdate.as_view(), name='edit_review'),
    path('book/<int:book_id>/review/<int:pk>/delete/', views.DeleteReviewView.as_view(), name='delete_review'),
]

