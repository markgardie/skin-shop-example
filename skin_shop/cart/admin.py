from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


# -------------------------------
# CartItem Inline
# -------------------------------
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    autocomplete_fields = ["skin"]


# -------------------------------
# Cart Admin
# -------------------------------
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_quantity", "total_price", "updated_at")
    search_fields = ("user__email",)
    readonly_fields = ("created_at", "updated_at", "total_quantity", "total_price")
    inlines = [CartItemInline]


# -------------------------------
# OrderItem Inline
# -------------------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    autocomplete_fields = ["skin"]
    readonly_fields = ("price_at_purchase", "created_at", "updated_at")


# -------------------------------
# Order Admin
# -------------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total_price", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__email",)
    readonly_fields = ("created_at", "updated_at", "total_price")
    inlines = [OrderItemInline]

    actions = ["mark_completed", "mark_failed"]

    def mark_completed(self, request, queryset):
        queryset.update(status=Order.Status.COMPLETED)

    def mark_failed(self, request, queryset):
        queryset.update(status=Order.Status.FAILED)


# -------------------------------
# OrderItem Admin (optional)
# -------------------------------
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "skin", "status", "price_at_purchase")
    list_filter = ("status",)
    search_fields = ("order__id", "skin__name")