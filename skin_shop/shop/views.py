from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)

from .models import Skin
from .forms import SkinForm


class SkinListView(ListView):
    model = Skin
    template_name = "shop/skin_list.html"
    context_object_name = "skins"
    paginate_by = 12

    def get_queryset(self):
        return Skin.objects.filter(is_active=True).order_by("-created_at")

class SkinDetailView(DetailView):
    model = Skin
    template_name = "shop/skin_detail.html"
    context_object_name = "skin"


class SkinCreateView(LoginRequiredMixin, CreateView):
    model = Skin
    form_class = SkinForm
    template_name = "shop/skin_form.html"
    success_url = reverse_lazy("shop:skin_list")

class SkinUpdateView(LoginRequiredMixin, UpdateView):
    model = Skin
    form_class = SkinForm
    template_name = "shop/skin_form.html"
    context_object_name = "skin"
    success_url = reverse_lazy("shop:skin_list")


class SkinDeleteView(LoginRequiredMixin, DeleteView):
    model = Skin
    template_name = "shop/skin_confirm_delete.html"
    context_object_name = "skin"
    success_url = reverse_lazy("shop:skin_list")
