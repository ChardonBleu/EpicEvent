from django.urls import path, include
from rest_framework.routers import DefaultRouter

from CRM.views import CustomerViewSet


router = DefaultRouter()
router.register('customers', CustomerViewSet, basename='customer')



urlpatterns = [

    path('', include(router.urls)),

]

