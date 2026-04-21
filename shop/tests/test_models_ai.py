import pytest
from shop.tests.factories import BookFactory, OrderFactory
from asgiref.sync import sync_to_async

@pytest.mark.django_db
def test_book_str_ai():
    """
    Generated with AI, reviewed and modified
    """
    book = BookFactory(title="AI Generated Title")
    assert str(book) == "AI Generated Title"

@pytest.mark.django_db
def test_order_paid_status_ai():
    """
    Generated with AI, reviewed and modified
    """
    order = OrderFactory(paid=False)
    assert order.paid is False