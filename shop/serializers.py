from rest_framework import serializers
from .models import Book, Category, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "price",
            "category",
            "category_id",
            "stock",
            "description",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "book", "price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["created_at"]
