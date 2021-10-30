from django.contrib import admin

from .models import Custumer


@admin.register(Custumer)
class CustumerAdmin(admin.ModelAdmin):
    """
    Link a CustumUser to the Admin panel, ensuring the encryption of
    passwords.


    Arguments:
        UserAdmin {[type]} -- [description]
    """
    list_display = ('id', 'full_name', 'email', 'mobile', 
                    'datetime_created', 'datetime_updated')
    list_display_links = ('id', 'full_name',)
    empty_value_display = "Inconnu"
    search = ('first_name')
    list_filter = ('sales_customuser',)
    
