from django.db import models
from django.utils.text import slugify


class SkinCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Skin Category"
        verbose_name_plural = "Skin Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SkinTag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=40, unique=True, blank=True)

    class Meta:
        verbose_name = "Skin Tag"
        verbose_name_plural = "Skin Tags"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Skin(models.Model):
    class SkinType(models.TextChoices):
        REGULAR = "regular", "Regular Skin"
        HD = "hd", "HD Skin"
        CAPE = "cape", "Cape"
        SPECIAL = "special", "Special / Event"

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    category = models.ForeignKey(
        SkinCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="skins"
    )

    tags = models.ManyToManyField(SkinTag, blank=True)

    type = models.CharField(
        max_length=20,
        choices=SkinType.choices,
        default=SkinType.REGULAR
    )

    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    image = models.ImageField(upload_to="skins/previews/")
    file = models.FileField(
        upload_to="skins/files/",
        help_text="Скін у форматі PNG"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Skin"
        verbose_name_plural = "Skins"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
