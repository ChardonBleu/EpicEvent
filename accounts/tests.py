import pytest
from django.test import Client

from models import CustomUser


@pytest.fixture
def client(db):
    return Client()


# ################################################################# #
# ################## TEST connexion admin panel ################### #


def test_unauthorized_user_on_admin(client: Client):
    response = client.get('/admin/')
    assert response.status_code == 302


def test_superuser_on_admin(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200

