import pytest
from django.test import Client

from CRM.models import Custumer
from accounts.models import CustomUser


# ############################################################# #
# ########################  FIXTURES   ######################## #

@pytest.fixture
def vendeur1(db):
    return CustomUser.objects.create_user(username="vendeur1",
                                          password="vend1PassTest",
                                          email="vend1@soleneidos.fr")

@pytest.fixture
def suppport1(db):
    return CustomUser.objects.create_user(username="support1",
                                          password="sup1PassTest",
                                          email="sup1@soleneidos.fr")

@pytest.fixture
def client(db):
    return Client()

@pytest.fixture
def custumer1(db, vendeur1: CustomUser):
    return Custumer.objects.create(first_name="Lulu",
                                   last_name="Lefetard",
                                   email="lulu@soleneidos.fr",
                                   mobile="123456789",
                                   sales_customuser=vendeur1)

# ############################################################# #
# ####################  TEST STR models   ##################### #


def test_str_custumer(custumer1: Custumer):
    assert str(custumer1) == "Lulu Lefetard"

def test_full_name(custumer1: Custumer):
    assert custumer1.full_name == "Lulu LEFETARD"