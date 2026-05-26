from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Book


@receiver([post_save, post_delete], sender=Book)
def invalidate_book_cache(sender, instance, **kwargs):
    cache.delete(f"book_detail_{instance.id}")
    cache.delete("books_list_cache")
