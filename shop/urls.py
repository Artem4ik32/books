from django.urls import path
from .views import *
from .views import create_checkout_session

app_name = "shop"

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("book/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("book/create/", BookCreateView.as_view(), name="book_create"),
    path("book/<int:pk>/update/", BookUpdateView.as_view(), name="book_update"),
    path("book/<int:pk>/delete/", BookDeleteView.as_view(), name="book_delete"),

    path("cart/", cart_detail, name="cart_detail"),
    path("cart/add/<int:book_id>/", cart_add, name="cart_add"),
    path("cart/remove/<int:book_id>/", cart_remove, name="cart_remove"),

    path("order/create/", create_order, name="create_order"),
    path("checkout/", create_checkout_session, name="checkout"),
]