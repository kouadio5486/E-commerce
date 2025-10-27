from rest_framework import routers
from django.urls import path, include
from .views import (
    ProductViewSet,
    UserViewSet,
    OrderViewSet,
    CartViewSet,
    FavoriteViewSet,
    CreateOrderView,
)

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'users', UserViewSet)
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'carts', CartViewSet, basename='carts')
router.register(r'favorites', FavoriteViewSet, basename='favorites')

urlpatterns = [
    path('', include(router.urls)),
    path('orders/create/', CreateOrderView.as_view(), name='orders-create'),
]
