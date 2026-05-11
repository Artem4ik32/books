import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from shop.models import Category, Book, Order

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password123')

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(username='admin', password='password123')

@pytest.fixture
def category(db):
    return Category.objects.create(name='Test Category')

@pytest.fixture
def book(db, category):
    return Book.objects.create(category=category, title='Test Book', author='Author', price=100, stock=5)

@pytest.mark.django_db
class TestAPI:
    def test_list_books(self, api_client, book):
        res = api_client.get('/api/books/')
        assert res.status_code == 200

    def test_search_books(self, api_client, book):
        res = api_client.get('/api/books/', {'search': 'Test'})
        assert res.status_code == 200

    def test_get_token(self, api_client, user):
        res = api_client.post('/api/token/', {'username': 'testuser', 'password': 'password123'})
        assert res.status_code == 200
        assert 'access' in res.data

    def test_user_sees_only_own_orders(self, api_client, user, admin_user):
        Order.objects.create(user=user) # Створюємо без address
        Order.objects.create(user=admin_user)
        api_client.force_authenticate(user=user)
        res = api_client.get('/api/orders/')
        assert res.data['count'] == 1

    def test_cors_headers(self, api_client):
        # CORS спрацьовує тільки якщо в запиті є заголовок Origin
        res = api_client.get('/api/books/', HTTP_ORIGIN='http://localhost')
        assert res.status_code == 200
        assert 'Access-Control-Allow-Origin' in res

    def test_swagger_ui(self, api_client):
        res = api_client.get('/api/docs/')
        assert res.status_code in [200, 302]


    def test_admin_can_create_book(self, api_client, admin_user, category):
        api_client.force_authenticate(user=admin_user)
        data = {
            'title': 'New API Book', 
            'author': 'AI', 
            'price': '99.99', 
            'category_id': category.id, 
            'stock': 10
        }
        res = api_client.post('/api/books/', data)
        assert res.status_code == 201

    def test_throttling_smoke(self, api_client):
        res = api_client.get('/api/books/')
        assert res.status_code == 200