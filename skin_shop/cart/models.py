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