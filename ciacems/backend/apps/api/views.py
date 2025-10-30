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

# ModelViewSet : toutes les actions CRUD sont disponibles.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # get_permissions: Méthode spéciale : change les permissions selon l’action.
    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAdminUser()]
        return super().get_permissions()


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
    # Chaque utilisateur ne voit que ses favoris 
        return Favorite.objects.filter(user=self.request.user)
    #  Récupère le product envoyé par le client.
    def create(self, request, *args, **kwargs):
        product_id = request.data.get("product")
        if not product_id:
            return Response({"error": "product est requis"}, status=status.HTTP_400_BAD_REQUEST)
           # Si le produit est déjà dans les favoris, on ne crée pas un doublon (get_or_create)
        fav, created = Favorite.objects.get_or_create(user=request.user, product_id=product_id)
        serializer = self.get_serializer(fav)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

#Gère le panier de l’utilisateur connecté.
#Chaque utilisateur voit uniquement son panier
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        #Le panier affiché est celui du user connecté.
        return CartItem.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        #Récupère le product et la quantity depuis le body.
        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))
        #Si le produit est déjà dans le panier, on augmente la quantité.
        if not product_id:
            return Response({"error": "product est requis"}, status=status.HTTP_400_BAD_REQUEST)
        item, created = CartItem.objects.get_or_create(user=request.user, product_id=product_id, defaults={"quantity": quantity})
        #Sinon, on crée une nouvelle ligne de panier.
        if not created:
            item.quantity += max(quantity, 1)
            item.save(update_fields=["quantity"])
        serializer = self.get_serializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

#Permet de voir les commandes
#Les utilisateurs normaux ne voient que leurs commandes.
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
                price = item.product.price  
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