from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView, UpdateView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import UserRegistrationForm, UserLoginForm, ProfileForm
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

class ProfileDetailView(LoginRequiredMixin, DetailView):
    """Перегляд профілю користувача."""
    model = User
    template_name = "users/profile_detail.html"
    context_object_name = "user_profile"

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редагування профілю користувача."""
    model = User
    form_class = ProfileForm
    template_name = "users/profile_update.html"
    success_url = reverse_lazy("users:profile_detail")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профіль успішно оновлено ✅")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Помилка при оновленні профілю.")
        return super().form_invalid(form)


