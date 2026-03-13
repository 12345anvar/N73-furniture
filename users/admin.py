from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # List page
    list_display = (
        'email',
        'full_name',
        'phone_number',
        'is_active',
        'is_staff',
        'created_at',
    )
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
    )
    search_fields = (
        'email',
        'full_name',
        'phone_number',
    )
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    # Detail / edit page
    fieldsets = (
        (None, {
            'fields': ('email', 'password'),
        }),
        (_('Personal information'), {
            'fields': ('full_name', 'phone_number'),
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'created_at', 'updated_at'),
        }),
    )

    # Add user page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'full_name',
                'phone_number',
                'password1',
                'password2',
                'is_active',
                'is_staff',
            ),
        }),
    )
