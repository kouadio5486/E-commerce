from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    autocomplete_fields = ("product",)
    fields = ("product", "quantity", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total", "date", "items_count")
    list_filter = ("date",)
    search_fields = ("user__email", "items__product__name")
    ordering = ("-date",)
    date_hierarchy = "date"
    list_select_related = ("user",)
    autocomplete_fields = ("user",)
    inlines = [OrderItemInline]

    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = "Items"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "price")
    search_fields = ("order__user__email", "product__name")
    list_select_related = ("order", "product")
    autocomplete_fields = ("order", "product")
