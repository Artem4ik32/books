from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Book(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name=_("Category")
    )
    title = models.CharField(_("Title"), max_length=200)
    author = models.CharField(_("Author"), max_length=100)
    price = models.DecimalField(_("Price"), max_digits=6, decimal_places=2)
    description = models.TextField(_("Description"))
    stock = models.PositiveIntegerField(_("Stock"))

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    paid = models.BooleanField(_("Paid"), default=False)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"{_('Order')} {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", verbose_name=_("Order")
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_("Book"))
    price = models.DecimalField(_("Price"), max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)

    def __str__(self):
        return f"{self.book.title} ({self.quantity})"
