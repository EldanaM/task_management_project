from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Task


class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'role', 'is_staff']
    list_filter = ['role']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name')}),
        ('Права', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_by', 'assigned_to', 'created_at']
    list_filter = ['status']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Task, TaskAdmin)