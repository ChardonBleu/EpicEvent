import pytest
from django.test import Client

from CRM.models import Customer, Contract, EventStatus, Event
from accounts.models import CustomUser


# ############################################################# #
# ########################  FIXTURES   ######################## #

@pytest.fixture
def client(db):
    return Client()


@pytest.fixture
def vendeur1(db):
    return CustomUser.objects.create_user(username="vendeur1",
                                          password="vend1PassTest",
                                          email="vend1@soleneidos.fr")


@pytest.fixture
def support1(db):
    return CustomUser.objects.create_user(username="support1",
                                          password="sup1PassTest",
                                          email="sup1@soleneidos.fr")


@pytest.fixture
def customer1(db, vendeur1: CustomUser):
    return Customer.objects.create(first_name="Lulu",
                                   last_name="Lefetard",
                                   email="lulu@soleneidos.fr",
                                   mobile="123456789",
                                   sales_customuser=vendeur1)


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
