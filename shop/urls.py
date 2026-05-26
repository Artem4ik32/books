from django.contrib import admin
from django.urls import path, include
from config.warehouse_views import warehouse_check_api
from rest_framework.routers import DefaultRouter
from shop.views import BookViewSet, CategoryViewSet, OrderViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r"books", BookViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"orders", OrderViewSet, basename="order")

def health_check(request):
    return JsonResponse({"status": "healthy"}, status=200)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("shop.urls")),
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # Має бути ось так, якщо маршрут прописаний у shop:
    path('api/warehouse/check/<int:book_id>/', warehouse_check_api, name='warehouse_check'),
]
