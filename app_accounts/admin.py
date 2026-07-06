from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from app_accounts.models import User

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
    search_fields = ['username', 'email']
    list_filter = ['role', 'is_active', 'is_staff']
    ordering = ['username']
