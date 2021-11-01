from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Link a CustumUser to the Admin panel, ensuring the encryption of
    passwords.
    """
    list_display = ('id', 'upper_username', 'user_role',
                    'is_superuser', 'is_active', 'email',)
    list_display_links = ('id', 'upper_username',)
    empty_value_display = "Inconnu"
    search_fields = ('username',)
    list_filter = ('is_superuser', 'is_active', 'groups',)
    list_editable = ('is_active',)
    fieldsets = (
        (None, {
            "fields": ('username', 'password', 'email', 'is_superuser',
                       'is_active', 'groups'),
            }),
        )

    @admin.display(description='Username')
    def upper_username(self, obj):
        return(obj.username.upper())
