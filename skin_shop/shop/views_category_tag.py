from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import SkinCategory, SkinTag
from .forms import SkinCategoryForm, SkinTagForm


@login_required
@require_POST
def create_category(request):
    form = SkinCategoryForm(request.POST)
    if form.is_valid():
        category = form.save()
        return JsonResponse({
            "success": True,
            "id": category.id,
            "name": category.name
        })
    return JsonResponse({"success": False, "errors": form.errors}, status=400)


@login_required
@require_POST
def delete_category(request):
    category_id = request.POST.get("id")
    if not category_id:
        return HttpResponseBadRequest("Missing ID")

    try:
        category = SkinCategory.objects.get(id=category_id)
        category.delete()
        return JsonResponse({"success": True})
    except SkinCategory.DoesNotExist:
        return HttpResponseBadRequest("Category not found")

def list_categories(request):
    data = [
        {"id": c.id, "name": c.name}
        for c in SkinCategory.objects.all().order_by("name")
    ]
    return JsonResponse({"categories": data})


@login_required
@require_POST
def create_tag(request):
    form = SkinTagForm(request.POST)
    if form.is_valid():
        tag = form.save()
        return JsonResponse({
            "success": True,
            "id": tag.id,
            "name": tag.name
        })
    return JsonResponse({"success": False, "errors": form.errors}, status=400)


@login_required
@require_POST
def delete_tag(request):
    tag_id = request.POST.get("id")
    if not tag_id:
        return HttpResponseBadRequest("Missing ID")

    try:
        tag = SkinTag.objects.get(id=tag_id)
        tag.delete()
        return JsonResponse({"success": True})
    except SkinTag.DoesNotExist:
        return HttpResponseBadRequest("Tag not found")


def list_tags(request):
    data = [
        {"id": t.id, "name": t.name}
        for t in SkinTag.objects.all().order_by("name")
    ]
    return JsonResponse({"tags": data})
