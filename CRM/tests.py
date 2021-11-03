import pytest
import pytest_postgresql
from django.contrib.auth.models import Group
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
def vendeur1(db, sale_group):
    CustomUser.objects.create_user(username="vendeur1",
                                          password="vend1PassTest",
                                          email="vend1@soleneidos.fr")
    vendeur1 = CustomUser.objects.get(username="vendeur1")
    vendeur1.groups.add(sale_group)
    return CustomUser.objects.get(username="vendeur1")

@pytest.fixture
def logged_vendeur1(client: APIClient, vendeur1):
    response = client.post('/login/',
                           {'username': 'vendeur1',
                           'password': 'vend1PassTest'})
    return response.data['access']

@pytest.fixture
def vendeur2(db, sale_group):
    CustomUser.objects.create_user(username="vendeur2",
                                          password="vend2PassTest",
                                          email="vend2@soleneidos.fr")
    vendeur2 = CustomUser.objects.get(username="vendeur2")
    vendeur2.groups.add(sale_group)
    return CustomUser.objects.get(username="vendeur2")

@pytest.fixture
def logged_vendeur2(client: APIClient, vendeur2):
    response = client.post('/login/',
                           {'username': 'vendeur2',
                           'password': 'vend2PassTest'})
    return response.data['access']

@pytest.fixture
def support1(db, support_group):
    CustomUser.objects.create_user(username="support1",
                                          password="sup1PassTest",
                                          email="sup1@soleneidos.fr")
    support1 = CustomUser.objects.get(username="support1")
    support1.groups.add(support_group)
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
def event_status1(db):
    return EventStatus.objects.create(status='En prépa')


@pytest.fixture
def event1(db, customer1: Customer, support1: CustomUser,
           event_status1: EventStatus):
    return Event.objects.create(attendees="200",
                                customer=customer1,
                                support_customuser=support1,
                                event_status=event_status1)


@pytest.fixture
def event_without_support(db, customer1: Customer, support1: CustomUser,
                          event_status1: EventStatus):
    return Event.objects.create(attendees="200",
                                customer=customer1,
                                event_status=event_status1)


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


def test_event_status(event_status1: EventStatus):
    assert str(event_status1) == "En prépa"


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
    response = client.get('/customers/14/')
    assert response.status_code == 200

def test_update_costumer_detail(client, logged_vendeur1, customer1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_vendeur1)
    response = client.put('/customers/15/',
                        {'first_name': "Lolo",
                         'last_name': "Lefetard",
                         'email': "lulumodif@soleneidos.fr",
                         'phone': ' ',
                         'mobile': "123456789",
                         'company_name': ' ',
                         }, format='json')
    assert response.status_code == 200

def test_partial_update_costumer_detail(client, logged_vendeur1, customer1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_vendeur1)
    response = client.patch('/customers/16/',
                        {'email': "lulumodif@soleneidos.fr"}, format='json')
    assert response.status_code == 200


def test_delete_costumer(client, logged_vendeur1, customer1):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + logged_vendeur1)
    response = client.delete('/customers/17/')
    assert response.status_code == 204