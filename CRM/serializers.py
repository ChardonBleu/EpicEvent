from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from accounts.models import CustomUser
from CRM.models import Customer, Contract, Event


class ContractSerializer(serializers.ModelSerializer):
    costumer = serializers.SlugRelatedField(read_only=True,
                                               slug_field='full_name')
    sales_costumuser = serializers.SlugRelatedField(read_only=True,
                                               slug_field='username')

    class Meta:
        model = Contract
        fields = ['id', 'datetime_created', 'date_time_updated', 'status_sign',
                  'amount', 'payment_due', 'costumer', 'sales_customuser']


class EventSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(read_only=True,
                                               slug_field='full_name')
    support_costumuser = serializers.SlugRelatedField(read_only=True,
                                               slug_field='username')
    event_status = serializers.SlugRelatedField(read_only=True,
                                               slug_field='status')

    class Meta:
        model = Event
        fields = ['id', 'datetime_created', 'datetime_updated', 'attendees',
                  'event_date', 'notes', 'custumer', 'support_customuser',
                  'event_status']    


class CustomerSerializer(serializers.ModelSerializer):
    sales_costumuser = serializers.SlugRelatedField(read_only=True,
                                               slug_field='username')
    contracts_costumer = StringRelatedField(many=True, read_only=True)
    events_customer = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'eamil', 'phone',
                  'mobile', 'company_name', 'datetime_created',
                  'datetime_updated', 'sales_costumuser', 'contracts_costumer',
                  'events_customer']
