from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

from CRM.models import Customer, Contract, Event, EventStatus
from CRM.serializers import CustomerDetailSerializer, CustomerListSerializer
from CRM.serializers import ContractSerializer, EventSerializer, EventStatusSerializer

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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name', 'email']

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


class ContractFilter(filters.FilterSet):
    min_amount = filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr='lte')
    min_date = filters.DateTimeFilter(field_name="datetime_created",
                                      lookup_expr='gte')
    max_date = filters.DateTimeFilter(field_name="datetime_created",
                                      lookup_expr='lte')

    class Meta:
        model = Contract
        fields = ['customer__last_name', 'customer__first_name',
                  'customer__email', 'min_date', 'max_date',
                  'min_amount', 'max_amount']


class ContractViewSet(viewsets.ModelViewSet):
    """
    When user from sale group create a contract he does it for one of his
    clients. When creating contracts, the sale_customuser field is filled on
    with logged user.
    """
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, CanManage]
    queryset = Contract.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractFilter

    def perform_create(self, serializer):
        """The user from sale group is automaticaly saved as the
        sale_customuser.

        Arguments:
            serializer  -- ProjectSerializer
        """
        serializer.save(sales_customuser=self.request.user)


class EventFilter(filters.FilterSet):
    min_date = filters.DateTimeFilter(field_name="event_date",
                                      lookup_expr='gte')
    max_date = filters.DateTimeFilter(field_name="event_date",
                                      lookup_expr='lte')

    class Meta:
        model = Event
        fields = ['customer__last_name', 'customer__first_name',
                  'customer__email', 'min_date', 'max_date']


class EventViewSet(viewsets.ModelViewSet):
    """
    When user from sale group create an event he does it for one of his
    clients. Then admin user gives a support user on event using admin panel.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, CanManage]
    queryset = Event.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter


class EventStatusViewSet(viewsets.ModelViewSet):
    """
    When user from sale group create an event he does it for one of his
    clients. Then admin user gives a support user on event using admin panel.
    """
    serializer_class = EventStatusSerializer
    queryset = EventStatus.objects.all()
    permission_classes = [AllowAny]
    http_method_names = ['get']