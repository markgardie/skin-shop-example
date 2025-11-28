from django.contrib import admin
from .models import Skin, SkinCategory, SkinTag


@admin.register(SkinCategory)
class SkinCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at", "slug")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)
    fields = ("name", "slug", "description", "is_active", "created_at", "updated_at")
    readonly_fields = ("slug", "created_at", "updated_at")



@admin.register(SkinTag)
class SkinTagAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at", "slug")
    search_fields = ("name",)
    ordering = ("name",)
    fields = ("name", "slug", "created_at", "updated_at")
    readonly_fields = ("slug", "created_at", "updated_at")


@admin.register(Skin)
class SkinAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "type", "price", "is_active", "created_at", "updated_at")
    list_filter = ("category", "type", "is_active")
    search_fields = ("name", "category__name", "tags__name")
    ordering = ("-created_at",)
    filter_horizontal = ("tags",)  # для зручного вибору тегів
    fields = (
        "name",
        "slug",
        "category",
        "tags",
        "type",
        "price",
        "image",
        "file",
        "is_active",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("slug", "created_at", "updated_at")
