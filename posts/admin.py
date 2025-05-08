from django.contrib import admin
from posts.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'author',
        'category',
        'content',
        'is_published',
        'created_at',
        'updated_at'
    )
