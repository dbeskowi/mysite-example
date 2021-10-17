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
        'created',
        'updated',
    )

    search_fields = (
        'title',
    )

# Register the `Post` model
admin.site.register(models.Post, PostAdmin)
