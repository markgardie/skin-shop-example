from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest

from .models import Cart, CartItem
from shop.models import Skin
from .forms import AddToCartForm, UpdateCartItemForm, RemoveFromCartForm


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
    quantity = form.cleaned_data["quantity"]

    skin = get_object_or_404(Skin, id=skin_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        skin=skin,
        defaults={"quantity": quantity}
    )

    if not created:
        item.quantity += quantity
        item.save()

    if request.htmx:
        return render(request, "cart/partials/cart_items.html", {"cart": cart})

    return redirect("cart:detail")


# ----------------------------
# 4) Оновлення кількості
# ----------------------------
@login_required
def update_cart_item(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")

    form = UpdateCartItemForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest("Invalid data")

    item_id = form.cleaned_data["item_id"]
    quantity = form.cleaned_data["quantity"]

    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.quantity = quantity
    item.save()

    cart = item.cart

    if request.htmx:
        return render(request, "cart/partials/cart_items.html", {"cart": cart})

    return redirect("cart:detail")


# ----------------------------
# 5) Видалення з корзини
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
