from rest_framework import serializers

from CRM.models import Customer, Contract, Event


class ContractSerializer(serializers.ModelSerializer):
    
    sales_customuser = serializers.SlugRelatedField(read_only=True,
                                               slug_field='username')

    class Meta:
        model = Contract
        fields = ['id', 'datetime_created', 'datetime_updated', 'status_sign',
                  'amount', 'payment_due', 'customer', 'sales_customuser']


class EventSerializer(serializers.ModelSerializer):

    support_customuser = serializers.SlugRelatedField(read_only=True,
                                               slug_field='username')
    event_status = serializers.SlugRelatedField(read_only=True,
                                               slug_field='status')

    class Meta:
        model = Event
        fields = ['id', 'datetime_created', 'datetime_updated', 'attendees',
                  'event_date', 'notes', 'customer', 'support_customuser',
                  'event_status']    


class CustomerListSerializer(serializers.ModelSerializer):
      
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone',
                  'mobile', 'company_name', 'datetime_created',
                  'datetime_updated', 'sales_customuser']

class CustomerDetailSerializer(serializers.ModelSerializer):
    
    contracts_customer = ContractSerializer(many=True, read_only=True)
    events_customer = EventSerializer(many=True, read_only=True)
    

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone',
                  'mobile', 'company_name', 'datetime_created',
                  'datetime_updated', 'sales_customuser', 'contracts_customer',
                  'events_customer']
