from django.urls import path
from .views import TestHomeView, RegisterView, CustomLoginView, CustomLogoutView

urlpatterns = [
    path("", TestHomeView.as_view(), name="home"),

    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
