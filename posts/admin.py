from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea
from django.core import serializers
from django.http import HttpResponse

from .models import Post

def action_hide(modeladmin, request, queryset):
    queryset.update(hidden=True)
action_hide.short_description = "Mark posts as hidden"
action_hide.is_admin = False

def action_force_hide(modeladmin, request, queryset):
    queryset.update(force_hidden=True)
action_force_hide.short_description = "Force mark posts as hidden"
action_force_hide.is_admin = True

def action_force_readonly(modeladmin, request, queryset):
    queryset.update(force_readonly=True)
action_force_readonly.short_description = "Force mark posts as read-only"
action_force_readonly.is_admin = True

def action_remove_hidden(modeladmin, request, queryset):
    queryset.update(hidden=False)
action_remove_hidden.short_description = "Remove hidden mark from posts"
action_remove_hidden.is_admin = False

def action_remove_force_hidden(modeladmin, request, queryset):
    queryset.update(force_hidden=False)
action_remove_force_hidden.short_description = "Remove force-hidden mark from posts"
action_remove_force_hidden.is_admin = True

def action_remove_force_readonly(modeladmin, request, queryset):
    queryset.update(force_readonly=False)
action_remove_force_readonly.short_description = "Remove force-read-only mark from posts"
action_remove_force_readonly.is_admin = True

postadmin_actions = [
    action_hide,
    action_force_hide,
    action_force_readonly,
    action_remove_hidden,
    action_remove_force_hidden,
    action_remove_force_readonly,
]

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'ts']

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['author', 'title', 'text', 'image_url', 'image_file',
                    'hidden', 'force_hidden', 'force_readonly']
        else:
            return ['title', 'text', 'image_url', 'image_file', 'hidden']

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []

        if obj:
            return ['title', 'force_hidden', 'force_readonly']
        else:
            return ['force_hidden', 'force_readonly']

    def get_actions(self, request):
        actions = super().get_actions(request)

        if request.user.is_superuser:
            for act in postadmin_actions:
                actions[act.__name__] = (act, act.__name__, act.short_description)
        else:
            for act in postadmin_actions:
                if not act.is_admin:
                    actions[act.__name__] = (act, act.__name__, act.short_description)

        return actions

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
