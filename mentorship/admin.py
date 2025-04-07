from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Доп. поля', {'fields': ('phone', 'mentor')}),
    )
    list_display = ('username', 'email', 'phone', 'is_staff', 'is_mentor')
    search_fields = ('username', 'email', 'phone')
