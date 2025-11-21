from django import forms
from .models import Skin, SkinCategory, SkinTag

class SkinCategoryForm(forms.ModelForm):
    class Meta:
        model = SkinCategory
        fields = ["name", "description", "is_active"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Назва категорії"
            }),
            "description": forms.Textarea(attrs={
                "class": "textarea textarea-bordered w-full",
                "placeholder": "Опис (необов’язково)",
                "rows": 3
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "checkbox"
            }),
        }


class SkinTagForm(forms.ModelForm):
    class Meta:
        model = SkinTag
        fields = ["name"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Назва тегу"
            }),
        }


class SkinForm(forms.ModelForm):
    class Meta:
        model = Skin
        fields = [
            "name",
            "category",
            "tags",
            "type",
            "price",
            "image",
            "file",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Назва скіна"
            }),
            "category": forms.Select(attrs={
                "class": "select select-bordered w-full"
            }),
            "tags": forms.SelectMultiple(attrs={
                "class": "select select-bordered w-full h-40"
            }),
            "type": forms.Select(attrs={
                "class": "select select-bordered w-full"
            }),
            "price": forms.NumberInput(attrs={
                "class": "input input-bordered w-full",
                "step": "0.01",
                "placeholder": "Ціна"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "file-input file-input-bordered w-full"
            }),
            "file": forms.ClearableFileInput(attrs={
                "class": "file-input file-input-bordered w-full"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "checkbox"
            }),
        }

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if file and not file.name.lower().endswith(".png"):
            raise forms.ValidationError("Файл скіна повинен бути у форматі PNG.")
        return file
