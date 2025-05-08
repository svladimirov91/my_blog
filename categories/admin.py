from django.contrib import admin
from django.utils.text import slugify
from categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'owner', 'is_private')
    prepopulated_fields = {'slug': ('name',)}  # Автозаполнение

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)
