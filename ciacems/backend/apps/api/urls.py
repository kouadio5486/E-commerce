# Ils génèrent automatiquement les routes REST pour des ViewSet.
from rest_framework import routers
# Django pour déclarer des patterns d’URL.
from django.urls import path, include
from .views import (
    ProductViewSet,
    UserViewSet,
    OrderViewSet,
    CartViewSet,
    FavoriteViewSet,
    CreateOrderView,
)
# crée des routes REST standard et ajoute une vue navigable
router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'users', UserViewSet)
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'carts', CartViewSet, basename='carts')
router.register(r'favorites', FavoriteViewSet, basename='favorites')

urlpatterns = [
    # importe toutes les routes créées par DefaultRouter
    path('', include(router.urls)),
    path('orders/create/', CreateOrderView.as_view(), name='orders-create'),
    
     
]
