from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView

from .forms import UserRegistrationForm, UserLoginForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        """Після успішної реєстрації — автоматичний вхід користувача."""
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home")

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("home")

from django.views.generic import TemplateView


class TestHomeView(TemplateView):
    template_name = "test_home.html"

