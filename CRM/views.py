from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from CRM.models import Customer
from CRM.serializers import CustomerSerializer

    
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
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    

    def perform_create(self, serializer):
        """The author is automaticaly saved as the authenticated user

        Arguments:
            serializer  -- ProjectSerializer
        """
        serializer.save(sales_customuser=self.request.user)
