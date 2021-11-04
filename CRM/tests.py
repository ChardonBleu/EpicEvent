import pytest
import pytest_postgresql
from django.contrib.auth.models import Group, Permission
from rest_framework.test import APIClient

from CRM.models import Customer, Contract, EventStatus, Event
from accounts.models import CustomUser


# ############################################################# #
# ########################  FIXTURES   ######################## #

@pytest.fixture
def client(db):
    return APIClient()

@pytest.fixture
def sale_group(db):    
    sale_group = Group(name='sale')
    sale_group.save()
    return Group.objects.get(name='sale')

@pytest.fixture
def support_group(db):    
    support_group = Group(name='support')
    support_group.save()
    return Group.objects.get(name='support')

@pytest.fixture
def sale_permissions(db):
    view_customer = Permission.objects.get(codename='view_customer')
    view_contract = Permission.objects.get(codename='view_contract')
    view_event = Permission.objects.get(codename='view_event')

    add_customer = Permission.objects.get(codename='add_customer')
    add_contract = Permission.objects.get(codename='add_contract')
    add_event = Permission.objects.get(codename='add_event')

    change_customer = Permission.objects.get(codename='change_customer')
    change_contract = Permission.objects.get(codename='change_contract')
    change_event = Permission.objects.get(codename='change_event')

    sale_permissions = [
        view_customer,
        view_contract,
        view_event,
        add_customer,
        add_contract,
        add_event,
        change_customer,
        change_contract,
    ]
    return sale_permissions

@pytest.fixture
def support_permissions(db):
    view_customer = Permission.objects.get(codename='view_customer')
    view_contract = Permission.objects.get(codename='view_contract')
    view_event = Permission.objects.get(codename='view_event')

    change_event = Permission.objects.get(codename='change_event')

    support_permissions = [
        view_customer,
        view_contract,
        view_event,
        change_event,
    ]
    return support_permissions

@pytest.fixture
def vendeur1(db, sale_group, sale_permissions):
    CustomUser.objects.create_user(username="vendeur1",
                                          password="vend1PassTest",
                                          email="vend1@soleneidos.fr")
    vendeur1 = CustomUser.objects.get(username="vendeur1")
    vendeur1.groups.add(sale_group)
    vendeur1.user_permissions.set(sale_permissions)
    return CustomUser.objects.get(username="vendeur1")

@pytest.fixture
def logged_vendeur1(client: APIClient, vendeur1):
    response = client.post('/login/',
                           {'username': 'vendeur1',
                           'password': 'vend1PassTest'})
    return response.data['access']

@pytest.fixture
def vendeur2(db, sale_group, sale_permissions):
    CustomUser.objects.create_user(username="vendeur2",
                                          password="vend2PassTest",
                                          email="vend2@soleneidos.fr")
    vendeur2 = CustomUser.objects.get(username="vendeur2")
    vendeur2.groups.add(sale_group)
    vendeur2.user_permissions.set(sale_permissions)
    return CustomUser.objects.get(username="vendeur2")

@pytest.fixture
def logged_vendeur2(client: APIClient, vendeur2):
    response = client.post('/login/',
                           {'username': 'vendeur2',
                           'password': 'vend2PassTest'})
    return response.data['access']

@pytest.fixture
def support1(db, support_group, support_permissions):
    CustomUser.objects.create_user(username="support1",
                                          password="sup1PassTest",
                                          email="sup1@soleneidos.fr")
    support1 = CustomUser.objects.get(username="support1")
    support1.groups.add(support_group)
    support1.user_permissions.set(support_permissions)
    return CustomUser.objects.get(username="support1")

@pytest.fixture
def logged_support1(client: APIClient, support1):
    response = client.post('/login/',
                           {'username': 'support1',
                           'password': 'sup1PassTest'})
    return response.data['access']


@pytest.fixture
def customer1(db, vendeur1: CustomUser):
    return Customer.objects.create(first_name="Lulu",
                                   last_name="Lefetard",
                                   email="lulu@soleneidos.fr",
                                   mobile="123456789",
                                   sales_customuser=vendeur1)

@pytest.fixture
def customer2(db, vendeur2: CustomUser):
    return Customer.objects.create(first_name="Jojo",
                                   last_name="Aimelafete",
                                   email="jojo@soleneidos.fr",
                                   mobile="123456789",
                                   sales_customuser=vendeur2)


@pytest.fixture
def contract1(db, vendeur1: CustomUser, customer1: Customer):
    return Contract.objects.create(amount='10250.50',
                                   payment_due="2022-01-20",
                                   customer=customer1,
                                   sales_customuser=vendeur1)


@pytest.fixture
def status1(db):
    return EventStatus.objects.create(status='En prépa')


@pytest.fixture
def event1(db, customer1: Customer, support1: CustomUser,
           status1: EventStatus):
    return Event.objects.create(attendees="200",
                                customer=customer1,
                                support_customuser=support1,
                                status=status1)


@pytest.fixture
def event_without_support(db, customer1: Customer, support1: CustomUser,
                          status1: EventStatus):
    return Event.objects.create(attendees="200",
                                customer=customer1,
                                status=status1)


# ############################################################# #
# #############  TEST STR and @property models   ############## #


def test_str_customer(customer1: Customer):
    assert str(customer1) == "Lulu Lefetard"


def test_full_name(customer1: Customer):
    assert customer1.full_name == "Lulu LEFETARD"


def test_str_contact(contract1: Contract):
    assert str(contract1) == "Contracté pour Lulu Lefetard - 10250.50 $"


def test_description_contract(contract1: Contract):
    assert contract1.description == "Contracté pour Lulu Lefetard"


def test_event_status(status1: EventStatus):
    assert str(status1) == "En prépa"


def test_event(event1: Event):
    assert str(event1) == "Evènement commandé par Lulu Lefetard - suivi \
par support1"


def test_description_event(event1: Event):
    assert event1.description == "Evènement commandé par Lulu Lefetard - \
suivi par support1 - En prépa "


def test_event_has_support(event1: Event):
    assert event1.has_support is True


def test_event_has_not_support(event_without_support: Event):
    assert event_without_support.has_support is False

# ############################################################################
# ###########################  Tests CUSTOMERS  ##############################
# ############################################################################


def test_get_customer_list_for_sale_group(client, logged_vendeur1,
                                               customer1, customer2):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_vendeur1)
    response = client.get('/customers/')
    assert response.status_code == 200
    assert b'Jojo' in response.content
    assert b'Lulu' in response.content

def test_get_customer_list_for_support_group(client, logged_support1,
                                                   customer1, customer2):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_support1)
    response = client.get('/customers/')
    assert response.status_code == 200
    assert b'Jojo' in response.content
    assert b'Lulu' in response.content 

def test_sale_user_can_post_new_costumer(client, logged_vendeur1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_vendeur1)
    response = client.post('/customers/',
                           {'first_name': "Toto",
                            'last_name': "Lerigolo",
                            'email': "toto@soleneidos.fr",
                            'mobile': "123456789"}, format='json')
    assert response.status_code == 201

def test_support_not_authorized_to_post_new_costumer(client, logged_support1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_support1)
    response = client.post('/customers/',
                           {'first_name': "Toto",
                            'last_name': "Lerigolo",
                            'email': "toto@soleneidos.fr",
                            'mobile': "123456789"}, format='json')
    assert response.status_code == 403
    
def test_view_costumer_detail(client, logged_vendeur1, customer1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_vendeur1)
    
    response = client.get('/customers/' + str(customer1.id) +'/')
    assert response.status_code == 200

def test_update_costumer_detail(client, logged_vendeur1, customer1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_vendeur1)
    response = client.put('/customers/' + str(customer1.id) +'/',
                          {'first_name': "Lolo",
                           'last_name': "Lefetard",
                           'email': "lulumodif@soleneidos.fr",
                           'phone': ' ',
                           'mobile': "123456789",
                           'company_name': ' '}, format='json')
    assert response.status_code == 200

def test_partial_update_costumer_detail(client, logged_vendeur1, customer1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_vendeur1)
    response = client.patch('/customers/' + str(customer1.id) +'/',
                            {'email': "lulumodif@soleneidos.fr"}, format='json')
    assert response.status_code == 200


def test_delete_costumer(client, logged_vendeur1, customer1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_vendeur1)
    response = client.delete('/customers/' + str(customer1.id) + '/')
    assert response.status_code == 403


# ############################################################################
# ###########################  Tests CONTRACTS  ##############################
# ############################################################################


def test_get_contracts_list_for_sale_group(client, logged_vendeur1,
                                             contract1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_vendeur1)
    response = client.get('/contracts/')
    assert response.status_code == 200

def test_get_contracts_list_for_support_group(client, logged_support1,
                                             contract1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_support1)
    response = client.get('/contracts/')
    assert response.status_code == 200

def test_sale_user_can_post_new_contract(client, logged_vendeur1,
                                              customer1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_vendeur1)
    response = client.post('/contracts/',
                           {'amount': '1000.50',
                            'payment_due': "2022-02-12",
                            'customer': customer1.id}, format='json')
    assert response.status_code == 201

def test_support_not_authorized_to_post_new_contract(client,
                                                    logged_support1,
                                                    customer1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_support1)
    response = client.post('/contracts/',
                           {'status_sign': False,
                            'amount': "100",
                            'payment_due': "2022-03-20",
                            'customer': customer1.id}, format='json')
    assert response.status_code == 403

def test_view_contract_detail(client, logged_vendeur1, contract1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_vendeur1)
    response = client.get('/contracts/' + str(contract1.id) +'/')
    assert response.status_code == 200

def test_update_contract_detail(client, logged_vendeur1,
                                   contract1, customer1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_vendeur1)
    response = client.put('/contracts/' + str(contract1.id) +'/',
                           {'status_sign': True,
                            'amount': '10250.50',
                            'payment_due': "2022-01-20",
                            'customer': customer1.id}, format='json')
    assert response.status_code == 200

def test_partial_update_contract_detail(client, logged_vendeur1, contract1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_vendeur1)
    response = client.patch('/contracts/' + str(contract1.id) +'/',
                            {'status_sign': True,}, format='json')
    assert response.status_code == 200

def test_CANT_delete_contract(client, logged_vendeur1, contract1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_vendeur1)
    response = client.delete('/contracts/' + str(contract1.id) +'/')
    assert response.status_code == 403


# ############################################################################
# #############################  Tests EVENTS  ###############################
# ############################################################################


def test_get_events_list_for_sale_group(client, logged_vendeur1,
                                             event1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_vendeur1)
    response = client.get('/events/')
    assert response.status_code == 200

def test_get_events_list_for_support_group(client, logged_support1,
                                             event1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_support1)
    response = client.get('/events/')
    assert response.status_code == 200

def test_sale_user_can_post_new_event(client, logged_vendeur1,
                                    customer1, status1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_vendeur1)
    response = client.post('/events/',
                           {'attendees': '160',
                            'event_date': "2022-02-12",
                            'notes': 'event test',
                            'status': status1.id,
                            'customer': customer1.id}, format='json')
    assert response.status_code == 201

def test_support_not_authorized_to_post_new_event(client,
                                                    logged_support1,
                                                    customer1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_support1)
    response = client.post('/events/',
                           {'attendees': '160',
                            'event_date': "2022-02-12",
                            'notes': 'event test',
                            'customer': customer1.id}, format='json')
    assert response.status_code == 403

def test_sale_user_can_view_event_detail(client, logged_vendeur1, event1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_vendeur1)
    response = client.get('/events/' + str(event1.id) +'/')
    assert response.status_code == 200

def test_support_user_can_view_event_detail(client, logged_support1, event1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_support1)
    response = client.get('/events/' + str(event1.id) +'/')
    assert response.status_code == 200

def test_update_event_detail(client, logged_support1,
                                   event1, customer1,
                                   status1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_support1)
    response = client.put('/events/' + str(event1.id) +'/',
                           {'attendees': 200,
                            'status': status1.id,
                            'customer': customer1.id}, format='json')
    assert response.status_code == 200
    

def test_partial_update_event_detail(client, logged_support1, event1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_support1)
    response = client.patch('/events/' + str(event1.id) +'/',
                            {'notes': 'new notes'}, format='json')
    assert response.status_code == 200

def test_CANT_delete_event(client, logged_support1, event1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_support1)
    response = client.delete('/events/' + str(event1.id) +'/')
    assert response.status_code == 403
