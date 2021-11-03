from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from CRM.models import Customer, Contract
from CRM.serializers import CustomerDetailSerializer, CustomerListSerializer, ContractSerializer
from CRM.serializers import ContractSerializer

from CRM.permissions import CanAddOrUpdateCustomer
    
class CustomerViewSet(viewsets.ModelViewSet):
    """
    The endpoint [customers list](/customers/) is the main entry point of the
    **EpicEvent API**.

    The EpicEvent API is a RESTful API built using Django Rest Framework. It's
    part of project 12 of Openclassrooms formation Pyhton Developpers.

    You need to be authenticated to see customers list.

    Adlmin team manage users with django admin panel.
    Every user can login with username and password for the first login.
    You'll have then to use a [token](/token/) for authentication.
    After the first use of token access you'll have to
    [refresh](/token/refresh/) it.

    All users (from sale or support group) can see customers, contracts and
    events lists.

    """
    
    permission_classes = [IsAuthenticated, CanAddOrUpdateCustomer]    
      
    def get_serializer_class(self):
        if self.action == 'list':
            return CustomerListSerializer
        else:
            return CustomerDetailSerializer


    def get_queryset(self):
        if self.action == 'list' or self.action == 'retrieve':
            return Customer.objects.all()
        else:
            return Customer.objects.filter(sales_customuser=self.request.user)


class ContractViewSet(viewsets.ModelViewSet):
    """
    When user from sale group create a contract he does it for one of his
    clients. When creating contracts, the sale_customuser field is filled on
    with logged user.    

    """
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Contract.objects.all()
    

    def perform_create(self, serializer):
        """The author is automaticaly saved as the authenticated user

        Arguments:
            serializer  -- ProjectSerializer
        """
        serializer.save(sales_customuser=self.request.user)