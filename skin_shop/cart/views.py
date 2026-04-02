from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest

from .models import Cart, CartItem, Order, OrderItem
from shop.models import Skin
from .forms import AddToCartForm, RemoveFromCartForm
from minecraft.services import apply_skins_for_order


# ----------------------------
# 1) Повна сторінка корзини
# ----------------------------
@login_required
def cart_page(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart/detail.html", {"cart": cart})


# ----------------------------
# 2) Partial для HTMX-запитів
# ----------------------------
@login_required
def cart_items(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart/partials/cart_items.html", {"cart": cart})


# ----------------------------
# 3) Додавання в корзину
# ----------------------------
@login_required
def add_to_cart(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")

    form = AddToCartForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest("Invalid data")

    skin_id = form.cleaned_data["skin_id"]
    skin = get_object_or_404(Skin, id=skin_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    CartItem.objects.get_or_create(cart=cart, skin=skin)

    if request.htmx:
        return render(request, "cart/partials/cart_items.html", {"cart": cart})

    return redirect("cart:detail")


# ----------------------------
# 4) Видалення з корзини
# ----------------------------
@login_required
def remove_from_cart(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")

    form = RemoveFromCartForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest("Invalid data")

    item_id = form.cleaned_data["item_id"]
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart = item.cart

    item.delete()

    if request.htmx:
        return render(request, "cart/partials/cart_items.html", {"cart": cart})

    return redirect("cart:detail")


# ----------------------------
# 5) Оформлення замовлення
# ----------------------------
@login_required
def checkout(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")

    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.select_related("skin").all()

    if not items.exists():
        return redirect("cart:detail")

    # Створюємо замовлення
    order = Order.objects.create(user=request.user)

    for item in items:
        OrderItem.objects.create(
            order=order,
            skin=item.skin,
            price_at_purchase=item.skin.price,
        )

    # Очищаємо корзину
    items.delete()

    # Застосовуємо скіни на сервері
    apply_skins_for_order(order)

    return redirect("cart:order_success", pk=order.pk)


# ----------------------------
# 6) Сторінка успішного замовлення
# ----------------------------
@login_required
def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, "cart/order_success.html", {"order": order})


@login_required
def order_list(request):
    orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related("order_items__skin")
        .order_by("-created_at")
    )

    return render(request, "cart/order_list.html", {"orders": orders})

