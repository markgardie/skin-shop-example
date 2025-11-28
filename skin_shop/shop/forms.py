from django import forms
from .models import SkinCategory, SkinTag, Skin


BASE_INPUT = (
    "w-full bg-gray-700 text-white border border-gray-600 rounded-lg px-3 py-2 "
    "focus:outline-none focus:ring-2 focus:ring-blue-500"
)

BASE_TEXTAREA = (
    "w-full bg-gray-700 text-white border border-gray-600 rounded-lg px-3 py-2 "
    "focus:outline-none focus:ring-2 focus:ring-blue-500"
)

BASE_SELECT = (
    "w-full bg-gray-700 text-white border border-gray-600 rounded-lg px-3 py-2 "
    "focus:outline-none focus:ring-2 focus:ring-blue-500"
)

BASE_FILE = (
    "block w-full text-sm text-gray-300 "
    "file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 "
    "file:text-sm file:font-semibold "
    "file:bg-minecraft-green file:text-black "
    "hover:file:bg-green-400"
)


class SkinCategoryForm(forms.ModelForm):
    class Meta:
        model = SkinCategory
        fields = ["name", "description", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({
            "class": BASE_INPUT,
            "placeholder": "Назва категорії"
        })

        self.fields["description"].widget.attrs.update({
            "class": BASE_TEXTAREA,
            "placeholder": "Опис (необов’язково)",
            "rows": 3
        })

        self.fields["is_active"].widget.attrs.update({
            "class": "checkbox"
        })

        for field in self.fields.values():
            field.label_suffix = ""


class SkinTagForm(forms.ModelForm):
    class Meta:
        model = SkinTag
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({
            "class": BASE_INPUT,
            "placeholder": "Назва тегу",
        })

        for field in self.fields.values():
            field.label_suffix = ""


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Text fields
        self.fields["name"].widget.attrs.update({
            "class": BASE_INPUT,
            "placeholder": "Назва скіна"
        })

        self.fields["price"].widget.attrs.update({
            "class": BASE_INPUT,
            "placeholder": "Ціна",
            "step": "0.01",
        })

        # Select fields
        self.fields["category"].widget.attrs.update({
            "class": BASE_SELECT
        })

        self.fields["tags"].widget.attrs.update({
            "class": BASE_SELECT + " h-40"
        })

        self.fields["type"].widget.attrs.update({
            "class": BASE_SELECT
        })

        # File fields
        self.fields["image"].widget.attrs.update({
            "class": BASE_FILE
        })

        self.fields["file"].widget.attrs.update({
            "class": BASE_FILE
        })

        # Checkbox
        self.fields["is_active"].widget.attrs.update({
            "class": "checkbox"
        })

        # Remove ":" after labels
        for field in self.fields.values():
            field.label_suffix = ""

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if file and not file.name.lower().endswith(".png"):
            raise forms.ValidationError("Файл скіна повинен бути у форматі PNG.")
        return file
