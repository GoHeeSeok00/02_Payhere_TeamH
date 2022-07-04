from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from user.models import User as UserModel


class CustomUserAdmin(BaseUserAdmin):
    """
    Assignee : 희석

    UserAdmin을 상속받아 커스텀한 클래스입니다.
    """

    model = UserModel
    ordering = ("created_at",)

    list_display = ("id", "email", "username", "is_active", "is_admin", "last_login", "created_at")
    list_display_links = ("id", "email")
    list_filter = ("is_active", "is_admin", "last_login")
    search_fields = ("username",)
    readonly_fields = ("created_at",)

    fieldsets = (
        ("info", {"fields": ("email", "password", "username", "created_at", "updated_at", "last_login")}),
        ("permissions", {"fields": ("is_admin", "is_active")}),
    )

    filter_horizontal = []


# Unregister(Group)
admin.site.unregister(Group)

# Register your models here.
admin.site.register(UserModel, CustomUserAdmin)
