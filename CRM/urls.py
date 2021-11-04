from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from CRM.views import CustomerViewSet, ContractViewSet


customers_router = DefaultRouter()
customers_router.register('customers', CustomerViewSet, basename='customer')

simple_router = SimpleRouter()
simple_router.register('contracts', ContractViewSet, basename='contract')



urlpatterns = [
    path('', include(customers_router.urls)),
    path('', include(simple_router.urls)),
]

