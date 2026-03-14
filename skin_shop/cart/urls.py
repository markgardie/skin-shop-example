from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_page, name="detail"),         # повна сторінка
    path("items/", views.cart_items, name="items"),   # HTMX partial
    path("add/", views.add_to_cart, name="add"),
    path("remove/", views.remove_from_cart, name="remove"),
]
