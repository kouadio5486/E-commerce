from django.contrib import admin

# Register your models here.
from .models import CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity")
    search_fields = ("user__email", "product__name")
    ordering = ("-id",)
    list_select_related = ("user", "product")
    raw_id_fields = ("user", "product")
