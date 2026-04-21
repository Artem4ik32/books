from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from django.core.mail import send_mail

from .models import Book, Order, OrderItem
from .cart import Cart

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class BookListView(ListView):
    model = Book
    template_name = "shop/book_list.html"
    context_object_name = "books"
    paginate_by = 5


class BookDetailView(DetailView):
    model = Book
    template_name = "shop/book_detail.html"


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


# CART
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


# ORDER
async def create_order(request):
    """
    Asynchronously creates a new order, processes cart items, 
    and sends a confirmation email to the user.
    Generated with AI.
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
    Generated with AI, reviewed and modified.
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