from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import CustomUser, UserRole


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Link a CustumUser to the Admin panel, ensuring the encryption of
    passwords.
    """
    list_display = ('id', 'upper_username',
                    'is_superuser', 'is_active', 'role', 'email',)
    list_display_links = ('id', 'upper_username',)
    empty_value_display = "Inconnu"
    search_fields = ('username',)
    list_filter = ('is_superuser', 'is_active', 'groups', 'role',)
    list_editable = ('is_active', 'role',)

    @admin.display(description='Username')
    def upper_username(self, obj):
        return(obj.username.upper())


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """
    Link a UserRole to the Admin panel.
    """
    list_display = ('id', 'role',)
    empty_value_display = "Inconnu"
