from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомна модель користувача з логіном по email."""

    email = models.EmailField(unique=True, verbose_name="Email адреса")
    username = models.CharField(max_length=150, blank=True, verbose_name="Ім'я користувача")

    minecraft_uuid = models.CharField(max_length=36, blank=True, null=True, verbose_name="UUID Minecraft")
    minecraft_nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name="Нікнейм у грі")

    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Аватар")

    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

    def __str__(self):
        return self.email or self.username or f"User #{self.pk}"
