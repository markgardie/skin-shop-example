from django.urls import path
from .views import RegisterView, CustomLoginView, CustomLogoutView, ProfileUpdateView, ProfileDetailView

app_name = 'users'

urlpatterns = [

    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),

    path("profile/", ProfileDetailView.as_view(), name="profile_detail"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_update"),
]
