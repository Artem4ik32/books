from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    category = models.ForeignKey(
    Category,
    on_delete=models.CASCADE,
    related_name='books',
    null=True,
    blank=True
)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.title
