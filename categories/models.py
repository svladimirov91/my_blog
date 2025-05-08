from django.contrib.auth import get_user_model
from django.db import models
from core.models import TimestampedModel
from django.utils.text import slugify

class Category(TimestampedModel):
    name = models.CharField(
        max_length=30,
        unique=True,  # Запрещены дубликаты названий
        help_text='Название категории (макс. 30 символов)'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=False
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='categories',
        help_text='Владелец категории'
    )
    is_private = models.BooleanField(
        default=False,
        help_text='Видна только владельцу?'
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Описание (необязательно)'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Автоматическое создание slug при сохранении."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
