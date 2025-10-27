from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, viewsets
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from apps.products.models import Product, Favorite
from apps.cart.models import CartItem
from apps.orders.models import Order, OrderItem

from .serializers import (
    UserSerializer,
    ProductSerializer,
    FavoriteSerializer,
    CartItemSerializer,
    OrderSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Order.objects.all()
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)


class CreateOrderView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            return Response({"error": "Panier vide"}, status=400)

        total = sum([item.product.price * item.quantity for item in cart_items])
        order = Order.objects.create(user=user, total=total)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        cart_items.delete()  # vider le panier
        serializer = OrderSerializer(order)
        return Response({"message": "Commande validée", "order": serializer.data})