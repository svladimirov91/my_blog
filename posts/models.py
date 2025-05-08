import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from core.models import TimestampedModel, UUIDModel
from categories.models import Category


class Post(UUIDModel, TimestampedModel):
    """Модель поста с поддержкой категорий, тегов и статусов."""
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок',
        help_text='Не более 200 символов'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # Пост остаётся, если категорию удалят
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Категория'
    )
    content = models.TextField(verbose_name='Текст поста')
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликовано?'
    )

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-created_at']  # Сортировка по дате создания (новые сначала)
        indexes = [
            models.Index(fields=['slug'], name='post_slug_idx'),  # Индекс для поиска по slug
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Автогенерация slug при создании поста."""
        if not self.slug:
            self.slug = slugify(f'{self.title}-{uuid.uuid4().hex[:6]}')
        super().save(*args, **kwargs)

    def publish(self):
        """Метод для публикации поста."""
        self.is_published = True
        self.published_at = timezone.now()
        self.save()
