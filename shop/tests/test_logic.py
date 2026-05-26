import pytest
from django.urls import reverse
from django.core.mail import send_mail
from unittest.mock import patch
from shop.models import Book, Category, Order, OrderItem
from shop.tests.factories import BookFactory, CategoryFactory, UserFactory
from shop.forms import BookForm
from asgiref.sync import sync_to_async


@pytest.mark.django_db
class TestModels:
    def test_category_str(self):
        obj = CategoryFactory(name="Sci-Fi")
        assert str(obj) == "Sci-Fi"

    def test_book_str(self):
        obj = BookFactory(title="Django Async")
        assert str(obj) == "Django Async"

    def test_order_default_status(self):
        order = Order.objects.create()
        assert order.paid is False
        assert "Order" in str(order)

    def test_book_price_positive(self):
        book = BookFactory(price=19.99)
        assert book.price > 0

    def test_category_slug_unique(self):
        CategoryFactory(slug="tech")
        with pytest.raises(Exception):
            CategoryFactory(slug="tech")

    @pytest.mark.parametrize("price", [10.00, 25.50, 100.99])
    def test_book_different_prices(self, price):
        book = BookFactory(price=price)
        assert book.price == price


@pytest.mark.django_db
class TestForms:
    def test_book_form_valid(self):
        cat = CategoryFactory()
        form = BookForm(
            data={
                "category": cat.id,
                "title": "Test",
                "author": "Author",
                "price": 10.00,
                "description": "Desc",
                "stock": 5,
            }
        )
        assert form.is_valid()

    def test_book_form_invalid(self):
        form = BookForm(data={})
        assert not form.is_valid()


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_async_cart_add(async_client):
    book = await sync_to_async(BookFactory.create)()
    url = reverse("shop:cart_add", kwargs={"book_id": book.id})
    response = await async_client.get(url)
    assert response.status_code == 302


@pytest.mark.asyncio
@pytest.mark.django_db
@patch("shop.views.stripe.checkout.Session.create")
async def test_async_stripe_checkout(mock_stripe, async_client):
    mock_stripe.return_value.url = "http://fake-stripe.com"
    url = reverse("shop:checkout")
    response = await async_client.get(url)
    assert response.status_code == 302
    assert response.url == "http://fake-stripe.com"


@pytest.mark.asyncio
@pytest.mark.django_db
@patch("django.core.mail.send_mail")
async def test_async_order_creation(mock_mail, async_client):
    url = reverse("shop:create_order")
    response = await async_client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
class TestUserFlows:
    def test_book_detail_flow(self, client):
        book = BookFactory()
        url = reverse("shop:book_detail", kwargs={"pk": book.pk})
        response = client.get(url)
        assert response.status_code == 200
        assert book.title in response.content.decode()

    def test_admin_access_denied(self, client):
        response = client.get("/admin/")
        assert response.status_code == 302

    @pytest.mark.asyncio
    @patch("django.utils.asyncio.os.environ", {"DJANGO_ALLOW_ASYNC_UNSAFE": "true"})
    async def test_full_buy_flow(self, async_client):
        book = await sync_to_async(BookFactory.create)(price=10)
        with patch("shop.views.send_mail") as mock_mail:
            await async_client.get(
                reverse("shop:cart_add", kwargs={"book_id": book.id})
            )
            response = await async_client.get(reverse("shop:create_order"))

            assert response.status_code == 200
            count = await sync_to_async(Order.objects.count)()
            assert count >= 1
            assert mock_mail.called

    def test_i18n_switching(self, client):
        url = reverse("set_language")
        response = client.post(url, data={"language": "uk"})
        assert response.status_code == 302
