from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from CRM.views import CustomerViewSet, ContractViewSet, EventViewSet


customers_router = DefaultRouter()
customers_router.register('customers', CustomerViewSet, basename='customer')
customers_router.register('contracts', ContractViewSet, basename='contract')
customers_router.register('events', EventViewSet, basename='event')

urlpatterns = [
    path('', include(customers_router.urls)),
]
