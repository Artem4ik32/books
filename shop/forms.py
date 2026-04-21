from django import forms
from .models import Book
from django.utils.translation import gettext_lazy as _

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["category", "title", "author", "price", "description", "stock"]
        labels = {
            'title': _('Book Title'),
            'price': _('Price in USD'),
        }