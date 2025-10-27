from django.contrib import admin

# Register your models here.
from .models import Product, Favorite


class FavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 0
    autocomplete_fields = ("user",)
    fields = ("user",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "stock")
    search_fields = ("name",)
    list_filter = ("stock",)
    ordering = ("name",)
    inlines = [FavoriteInline]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product")
    search_fields = ("user__email", "product__name")
    list_select_related = ("user", "product")
    autocomplete_fields = ("user", "product")
