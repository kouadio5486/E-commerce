from rest_framework import routers
from django.urls import path, include
from .views import (
    ProductViewSet,
    UserViewSet,
    OrderViewSet,
    CartViewSet,
    FavoriteViewSet,
)

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'users', UserViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'carts', CartViewSet)
router.register(r'favorites', FavoriteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/', include('products.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('orders.urls')),
]
