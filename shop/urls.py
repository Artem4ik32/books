from django.urls import path
from .views import *

app_name = "shop"

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("book/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("book/create/", BookCreateView.as_view(), name="book_create"),
    path("book/<int:pk>/update/", BookUpdateView.as_view(), name="book_update"),
    path("book/<int:pk>/delete/", BookDeleteView.as_view(), name="book_delete"),
]
