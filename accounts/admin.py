from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Link a CustumUser to the Admin panel, ensuring the encryption of 
    passwords.
    

    Arguments:
        UserAdmin {[type]} -- [description]
    """
    pass


admin.site.register(CustomUser, CustomUserAdmin)