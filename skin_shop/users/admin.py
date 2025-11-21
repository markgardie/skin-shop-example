from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Налаштування відображення кастомної моделі користувача в адмінці."""

    ordering = ["email"]
    list_display = ["email", "username", "minecraft_nickname", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active"]
    search_fields = ["email", "username", "minecraft_nickname"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Особиста інформація"), {"fields": ("username", "avatar")}),
        (_("Minecraft"), {"fields": ("minecraft_uuid", "minecraft_nickname")}),
        (_("Доступи"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Дати"), {"fields": ("date_joined",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2", "is_active", "is_staff"),
            },
        ),
    )

    readonly_fields = ["date_joined"]
