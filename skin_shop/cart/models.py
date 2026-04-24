from django.db import models
from django.conf import settings
from shop.models import Skin


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return f"Cart of {self.user.email}"

    @property
    def total_quantity(self):
        return self.items.count()

    @property
    def total_price(self):
        return sum(item.skin.price for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    skin = models.ForeignKey(
        Skin,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ("cart", "skin")

    def __str__(self):
        return self.skin.name

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} — {self.user.email}"

    @property
    def total_price(self):
        return sum(item.price_at_purchase for item in self.order_items.all())

    def update_status(self):
        """Автоматично оновлює статус замовлення на основі статусів OrderItem."""
        statuses = set(self.order_items.values_list("status", flat=True))
        if statuses == {OrderItem.Status.APPLIED}:
            self.status = self.Status.COMPLETED
        elif OrderItem.Status.FAILED in statuses:
            self.status = self.Status.FAILED
        self.save()

class OrderItem(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPLIED = "applied", "Applied"
        FAILED = "failed", "Failed"

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items"
    )
    skin = models.ForeignKey(
        Skin,
        on_delete=models.PROTECT,
        related_name="order_items"
    )
    price_at_purchase = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"{self.skin.name} — {self.status}"