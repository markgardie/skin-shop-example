
from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_page, name="detail"),
    path("items/", views.cart_items, name="items"),
    path("add/", views.add_to_cart, name="add"),
    path("remove/", views.remove_from_cart, name="remove"),
    path("checkout/", views.checkout, name="checkout"),
    
    path("order/<int:pk>/success/", views.order_success, name="order_success"),
    path("orders/", views.order_list, name="order_list"),
    path("orders/partial/", views.order_list_partial, name="order_list_partial"),
    path("order/<int:pk>/cancel/", views.cancel_order, name="cancel_order"),
    path("order/<int:pk>/delete/", views.delete_order, name="delete_order"),
]
