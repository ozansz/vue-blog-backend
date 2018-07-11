from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea

from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'ts']

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['author', 'title', 'text', 'image_url', 'hidden',
                    'force_hidden', 'force_readonly']
        else:
            return ['title', 'text', 'image_url', 'hidden']

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []

        if obj:
            return ['title', 'force_hidden', 'force_readonly']
        else:
            return ['force_hidden', 'force_readonly']

    def has_add_permission(self, request):
        return (request.user.is_superuser or request.user.is_active)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            if obj.force_readonly:
                return False
            if request.user == obj.author:
                return True
            else:
                return False
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            if obj.force_readonly:
                return False
            if request.user == obj.author:
                return True
            else:
                return False
        else:
            return True

    def save_model(self, request, obj, form, change):
        """When creating a new object, set the author field.
        """
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(Post, PostAdmin)
