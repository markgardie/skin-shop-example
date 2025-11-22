from django.urls import path
from .views import (
    SkinListView, SkinDetailView,
    SkinCreateView, SkinUpdateView, SkinDeleteView
)
from .views_category_tag import (
    create_category, delete_category, list_categories,
    create_tag, delete_tag, list_tags
)

app_name = "shop"

urlpatterns = [
    path("", SkinListView.as_view(), name="skin_list"),
    path("create/", SkinCreateView.as_view(), name="skin_create"),
    path("<slug:slug>/edit/", SkinUpdateView.as_view(), name="skin_edit"),
    path("<slug:slug>/delete/", SkinDeleteView.as_view(), name="skin_delete"),
    path("<slug:slug>/", SkinDetailView.as_view(), name="skin_detail"),

    path("ajax/category/create/", create_category, name="category_create"),
    path("ajax/category/delete/", delete_category, name="category_delete"),
    path("ajax/category/list/", list_categories, name="category_list"),

    path("ajax/tag/create/", create_tag, name="tag_create"),
    path("ajax/tag/delete/", delete_tag, name="tag_delete"),
    path("ajax/tag/list/", list_tags, name="tag_list"),
]
