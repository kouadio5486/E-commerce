from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, viewsets, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.db import transaction
from decimal import Decimal

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAdminUser()]
        return super().get_permissions()


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get("product")
        if not product_id:
            return Response({"error": "product est requis"}, status=status.HTTP_400_BAD_REQUEST)
        fav, created = Favorite.objects.get_or_create(user=request.user, product_id=product_id)
        serializer = self.get_serializer(fav)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))
        if not product_id:
            return Response({"error": "product est requis"}, status=status.HTTP_400_BAD_REQUEST)
        item, created = CartItem.objects.get_or_create(user=request.user, product_id=product_id, defaults={"quantity": quantity})
        if not created:
            item.quantity += max(quantity, 1)
            item.save(update_fields=["quantity"])
        serializer = self.get_serializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


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
        with transaction.atomic():
            # Vérifier stock
            for ci in cart_items.select_related("product"):
                if ci.quantity > ci.product.stock:
                    return Response({"error": f"Stock insuffisant pour {ci.product.name}"}, status=400)

            order = Order.objects.create(user=user, total=Decimal("0"))
            total = Decimal("0")

            for item in cart_items.select_related("product"):
                price = item.product.price  # snapshot du prix
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=price,
                )
                # décrémenter le stock
                item.product.stock -= item.quantity
                item.product.save(update_fields=["stock"])
                total += price * item.quantity

            # Mettre à jour le total
            order.total = total
            order.save(update_fields=["total"])

            # vider le panier
            cart_items.delete()

        serializer = OrderSerializer(order)
        return Response({"message": "Commande validée", "order": serializer.data}, status=201)