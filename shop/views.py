from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book, Category, Order, OrderItem
from .cart import Cart
from .serializers import BookSerializer, CategorySerializer, OrderSerializer
from .permissions import IsOwnerOrReadOnly
from django.core.cache import cache
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class BookListView(ListView):
    model = Book
    template_name = "shop/book_list.html"
    context_object_name = "books"
    paginate_by = 5


class BookDetailView(DetailView):
    model = Book
    template_name = "shop/book_detail.html"
    def get_object(self):
        book_id = self.kwargs.get("pk")
        return cache.get_or_set(f'book_detail_{book_id}', super().get_object(), 3600)

class BookCreateView(CreateView):
    model = Book
    fields = ["category", "title", "author", "price", "description", "stock"]
    template_name = "shop/book_form.html"
    success_url = reverse_lazy("shop:book_list")


class BookUpdateView(UpdateView):
    model = Book
    fields = ["category", "title", "author", "price", "description", "stock"]
    template_name = "shop/book_form.html"
    success_url = reverse_lazy("shop:book_list")


class BookDeleteView(DeleteView):
    model = Book
    template_name = "shop/book_confirm_delete.html"
    success_url = reverse_lazy("shop:book_list")



def cart_add(request, book_id):
    cart = Cart(request)
    book = Book.objects.get(id=book_id)
    cart.add(book)
    return redirect("shop:cart_detail")


def cart_remove(request, book_id):
    cart = Cart(request)
    book = Book.objects.get(id=book_id)
    cart.remove(book)
    return redirect("shop:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "shop/cart.html", {"cart": cart})



async def create_order(request):
    """
    Asynchronously creates a new order, processes cart items, 
    and sends a confirmation email to the user.
    """
    cart = Cart(request)

    if len(cart) == 0:
        return redirect("shop:book_list")

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                book=item["book"],
                price=item["price"],
                quantity=item["quantity"]
            )

    send_mail(
        "New Order",
        f"Order {order.id} created",
        "admin@test.com",
        ["test@test.com"],
        fail_silently=True,
    )

    cart.clear()
    return render(request, "shop/order_success.html", {"order": order})


async def create_checkout_session(request):
    """
    Creates a Stripe checkout session in a non-blocking way.
    """
    cart = Cart(request)
    line_items = []

    for item in cart:
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item["book"].title,
                },
                "unit_amount": int(float(item["price"]) * 100),
            },
            "quantity": item["quantity"],
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url="http://localhost:8000/success/",
        cancel_url="http://localhost:8000/cancel/",
    )

    return redirect(session.url)



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'price']
    search_fields = ['title', 'author']
    ordering_fields = ['price']


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)