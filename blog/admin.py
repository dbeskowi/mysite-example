"""
    blog.admin
"""

from django.contrib import admin
from . import models

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    """
        PostAdmin
    """

    list_display = (
        'title',
        'author',
        'status',
        'created',
        'updated',
    )

    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )
    list_filter = (
        'status',
    )
    prepopulated_fields = {'slug': ('title',)}

# Register the `Post` model
admin.site.register(models.Post, PostAdmin)

@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    """
    TopicAdmin
    """

    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)}
