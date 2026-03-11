from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book, Category



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
    fields = ["title", "author", "price", "description", "stock"]  # category прибрали
    template_name = "shop/book_form.html"
    success_url = reverse_lazy("shop:book_list")

    def form_valid(self, form):
        category, created = Category.objects.get_or_create(
            name="Fantasy",
            slug="fantasy"
        )
        form.instance.category = category
        return super().form_valid(form)


class BookUpdateView(UpdateView):
    model = Book
    fields = ["category", "title", "author", "price", "description", "stock"]
    template_name = "shop/book_form.html"
    success_url = reverse_lazy("shop:book_list")


class BookDeleteView(DeleteView):
    model = Book
    template_name = "shop/book_confirm_delete.html"
    success_url = reverse_lazy("shop:book_list")