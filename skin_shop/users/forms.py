from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "you@example.com"
        })
    )
    first_name = forms.CharField(
        label="Ім’я",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Ім’я (необов’язково)"
        })
    )
    last_name = forms.CharField(
        label="Прізвище",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Прізвище (необов’язково)"
        })
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Введіть пароль"
        })
    )
    password2 = forms.CharField(
        label="Підтвердіть пароль",
        widget=forms.PasswordInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Повторіть пароль"
        })
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # на випадок, якщо поле username залишилось у базі
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": (
                    "w-full bg-gray-700 text-white border border-gray-600 "
                    "rounded-lg px-3 py-2 focus:outline-none "
                    "focus:ring-2 focus:ring-blue-500"
                )
            })
            field.label_suffix = ""  # прибирає двокрапку після label


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "you@example.com"
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Введіть пароль"
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": (
                    "w-full bg-gray-700 text-white border border-gray-600 "
                    "rounded-lg px-3 py-2 focus:outline-none "
                    "focus:ring-2 focus:ring-blue-500"
                )
            })
            field.label_suffix = ""

class ProfileUpdateForm(forms.ModelForm):
    """Форма для редагування профілю користувача."""

    class Meta:
        model = User
        fields = ["username", "email", "avatar", "minecraft_nickname", "minecraft_uuid"]
        labels = {
            "username": "Ім'я користувача",
            "email": "Email",
            "avatar": "Аватар",
            "minecraft_nickname": "Нік у грі",
            "minecraft_uuid": "UUID Minecraft",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            base_classes = (
                "w-full bg-gray-700 text-white border border-gray-600 "
                "rounded-lg px-3 py-2 focus:outline-none focus:ring-2 "
                "focus:ring-blue-500"
            )

            if isinstance(field.widget, forms.FileInput):
                # окремий стиль для file input
                field.widget.attrs.update({
                    "class": "block w-full text-sm text-gray-300 "
                             "file:mr-4 file:py-2 file:px-4 "
                             "file:rounded-lg file:border-0 "
                             "file:text-sm file:font-semibold "
                             "file:bg-minecraft-green file:text-black "
                             "hover:file:bg-green-400"
                })
            else:
                field.widget.attrs.update({"class": base_classes})

            field.label_suffix = ""