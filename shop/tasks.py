from celery import shared_task
from django.core.mail import send_mail
from django.contrib.sessions.models import Session
from django.utils import timezone
from .models import Book

@shared_task
def send_order_email_task(order_id, user_email):
    send_mail(
        "Order Confirmation",
        f"Order #{order_id} has been placed.",
        "admin@shop.com",
        [user_email],
    )

@shared_task
def generate_report_task():
    count = Book.objects.count()
    return f"Total books in library: {count}"

@shared_task
def clear_expired_sessions():
    Session.objects.filter(expire_date__lt=timezone.now()).delete()