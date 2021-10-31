from django.contrib import admin

from .models import Customer, Contract, EventStatus, Event


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Link Custumers on admin panel with personnal display

    """
    list_display = ('id', 'full_name', 'email', 'mobile',
                    'datetime_created', 'datetime_updated')
    list_display_links = ('id', 'full_name',)
    search_fields = ('last_name', 'first_name', 'datetime_created',
                     'sales_customuser__username',)
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
    search_fields = ('datetime_created', 'payment_due',
                     'sales_customuser__username', 'customer__last_name',
                     'customer__first_name',)
    list_filter = ('status_sign',)


@admin.register(EventStatus)
class EventStatusAdmin(admin.ModelAdmin):
    """
    Link EventStatus on admin panel with personnal display
    """

    list_display = ('id', 'status')
    list_display_links = ('id', 'status',)
    empty_value_display = "Inconnu"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Link Events on admin panel with personnal display
    """
    list_display = ('id', 'description', 'has_support', 'datetime_created', 'attendees',
                    'event_date', 'notes',)
    list_display_links = ('id', 'description',)
    empty_value_display = "Inconnu"
    search_fields = ('datetime_created', 'customer__last_name',
                     'customer__first_name', 'event_date',
                     'support_customuser__username')
    list_filter = ('event_status',)
