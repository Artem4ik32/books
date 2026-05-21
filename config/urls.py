from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns
from rest_framework.routers import DefaultRouter
from shop.views import BookViewSet, CategoryViewSet, OrderViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'orders', OrderViewSet, basename='order')

def health_check(request):
    return JsonResponse({"status": "healthy"}, status=200)

urlpatterns = [
    path('admin/', admin.site.side_effects if hasattr(admin, 'side_effects') else admin.site.urls), # твій адмін-панель
    path('health/', health_check, name='health_check'),

    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    
    path('api/', include(router.urls)),
    
    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Документація API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

urlpatterns += i18n_patterns(
    path("", include("shop.urls")),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    prefix_default_language=False
)