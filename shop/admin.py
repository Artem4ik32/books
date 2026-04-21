from django.contrib import admin
from .models import Book, Category, Order, OrderItem


class BookInline(admin.TabularInline):
    model = Book
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [BookInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "price", "stock", "category")
    list_filter = ("category", "price")
    search_fields = ("title", "author")
    list_editable = ("price", "stock")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created", "paid")
    list_filter = ("paid", "created")
    inlines = [OrderItemInline]