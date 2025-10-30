from django.db import models
from django.conf import settings
from apps.products.models import Product

#on_delete=models.CASCADE → si l’utilisateur est supprimé,
#tous ses articles de panier seront supprimés aussi.
class CartItem(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

# Create your models here.
