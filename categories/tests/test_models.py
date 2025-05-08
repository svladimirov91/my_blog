import pytest
from django.db import IntegrityError
from django.utils.text import slugify
from categories.models import Category
from django.contrib.auth import get_user_model


User = get_user_model()

@pytest.mark.django_db
def test_category_creation_sets_slug_and_timestamps():
    user = User.objects.create_user(username='testuser', password='psw123')
    category = Category.objects.create(name='Категория1', owner=user)

    assert category.slug == slugify('Категория1')
    assert category.created_at is not None
    assert category.updated_at is not None


@pytest.mark.django_db
def test_category_str_returns_name():
    user = User.objects.create_user(username='anotheruser', password='qwerty')
    category = Category.objects.create(name='Категория2', owner=user)
    assert str(category) == 'Категория2'


@pytest.mark.django_db
def test_category_unique_name():
    user = User.objects.create_user(username='owner', password='pass')
    name = 'Категория3'
    Category.objects.create(name=name, owner=user)

    with pytest.raises(IntegrityError):
        # Пробуем создать дубликат
        Category.objects.create(name=name, owner=user)


@pytest.mark.django_db
def test_category_unique_slug():
    user = User.objects.create_user(username='slugger', password='3210')
    Category.objects.create(name='Категория4', owner=user)

    with pytest.raises(IntegrityError):
        # Пробуем создать дубликат
        Category.objects.create(name='Категория4', owner=user)
