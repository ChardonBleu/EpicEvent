from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from CRM.models import Customer, Contract, Event
from CRM.serializers import CustomerDetailSerializer, CustomerListSerializer
from CRM.serializers import ContractSerializer, EventSerializer

from CRM.permissions import CanManage


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

    permission_classes = [IsAuthenticated, CanManage]

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
    permission_classes = [IsAuthenticated, CanManage]
    queryset = Contract.objects.all()

    def perform_create(self, serializer):
        """The user from sale group is automaticaly saved as the
        sale_customuser.

        Arguments:
            serializer  -- ProjectSerializer
        """
        serializer.save(sales_customuser=self.request.user)


class EventViewSet(viewsets.ModelViewSet):
    """
    When user from sale group create an event he does it for one of his
    clients. Then admin user gives a support user on event using admin panel.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, CanManage]
    queryset = Event.objects.all()
