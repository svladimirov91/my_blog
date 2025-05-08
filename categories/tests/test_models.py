import pytest
from django.utils.text import slugify
from categories.models import Category
from django.contrib.auth import get_user_model


User = get_user_model()

@pytest.mark.django_db
def test_category_creation_sets_slug_and_timestamps():
    user = User.objects.create_user(username='testuser', password='psw123')
    category = Category.objects.create(name='Тестовая категория', owner=user)

    assert category.slug == slugify('Тестовая категория')
    assert category.created_at is not None
    assert category.updated_at is not None


@pytest.mark.django_db
def test_category_str_returns_name():
    user = User.objects.create_user(username='anotheruser', password='qwerty')
    category = Category.objects.create(name='Категория', owner=user)
    assert str(category) == 'Категория'


@pytest.mark.django_db
def test_category_unique_name():
    user = User.objects.create_user(username='owner', password='pass')
    Category.objects.create(name='Уникальная', owner=user)

    with pytest.raises(Exception):
        # Пробуем создать дубликат
        Category.objects.create(name='Уникальная', owner=user)
