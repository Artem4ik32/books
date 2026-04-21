import factory
from django.contrib.auth.models import User
from shop.models import Category, Book, Order, OrderItem

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.Faker("email")

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    name = factory.Faker("word")
    slug = factory.Sequence(lambda n: f"category-{n}")

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book
    category = factory.SubFactory(CategoryFactory)
    title = factory.Faker("sentence", nb_words=3)
    author = factory.Faker("name")
    price = 100.00
    description = "Test description"
    stock = 10

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order
    paid = False   