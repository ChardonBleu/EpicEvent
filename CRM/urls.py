from django.urls import path, include
from rest_framework.routers import DefaultRouter

from CRM.views import CustomerViewSet, ContractViewSet, EventViewSet, EventStatusViewSet

customers_router = DefaultRouter()
customers_router.register('customers', CustomerViewSet, basename='customer')
customers_router.register('contracts', ContractViewSet, basename='contract')
customers_router.register('events', EventViewSet, basename='event')
customers_router.register('eventstatus', EventStatusViewSet, basename='eventstatus')

urlpatterns = [
    path('', include(customers_router.urls)),
]
