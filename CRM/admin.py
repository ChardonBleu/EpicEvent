from django.contrib import admin

from .models import Custumer, Contract


@admin.register(Custumer)
class CustumerAdmin(admin.ModelAdmin):
    """
    Link Custumers on admin panel with personnal display

    """
    list_display = ('id', 'full_name', 'email', 'mobile', 
                    'datetime_created', 'datetime_updated')
    list_display_links = ('id', 'full_name',)
    search_fields = ('last_name', 'first_name', 'datetime_created',)
    empty_value_display = "Inconnu"
    

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    """
    Link Contracts on admin panel with personnal display
    """
    list_display = ('id', 'description', 'datetime_created', 'status_sign',
                    'amount', 'payment_due', 'datetime_updated')
    list_display_links = ('id', 'description',)
    empty_value_display = "Inconnu"
    search_fields = ('datetime_created','payment_due')
    list_filter = ('status_sign',)
