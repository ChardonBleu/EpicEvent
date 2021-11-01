import pytest
from django.test import Client
from django.contrib.auth.models import Group

from .models import CustomUser


@pytest.fixture
def client(db):
    return Client()


@pytest.fixture
def user_without_group_not_admin(db):
    toto = CustomUser.objects.create(username="toto",
                                     password='totopasstest',
                                     email="toto@soleneidos.fr",
                                     is_superuser=False)
    return toto


@pytest.fixture
def user_is_admin(db):
    return CustomUser.objects.create(username="sale1",
                                     password='sale1passtest',
                                     email="sale1@soleneidos.fr",
                                     is_superuser=True)


@pytest.fixture
def sale_group(db):
    sale_group = Group(name='sale')
    sale_group.save()
    return sale_group


@pytest.fixture
def support_group(db):
    support_group = Group(name='support')
    support_group.save()
    return support_group


@pytest.fixture
def user_in_sale_group(db, sale_group):
    sale_user = CustomUser.objects.create(username="sale1",
                                     password='sale1passtest',
                                     email="sale1@soleneidos.fr",
                                     is_superuser=False)
    sale_user.groups.add(sale_group)
    return sale_user


@pytest.fixture
def user_in_support_group(db, support_group):
    support_user = CustomUser.objects.create(username="support1",
                                             password='support1passtest',
                                             email="support1@soleneidos.fr",
                                             is_superuser=False)
    support_user.groups.add(support_group)
    return support_user


@pytest.fixture
def user_in_two_groups(db, support_group, sale_group):
    error_user = CustomUser.objects.create(username="support1",
                                             password='support1passtest',
                                             email="support1@soleneidos.fr",
                                             is_superuser=False)
    error_user.groups.add(support_group)
    error_user.groups.add(sale_group)
    return error_user


# ################################################################# #
# ################## TEST connexion admin panel ################### #


def test_unauthorized_user_on_admin(client: Client):
    response = client.get('/admin/')
    assert response.status_code == 302


def test_superuser_on_admin(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200

# ############################################################# #
# #############  TEST STR and @property models   ############## #


def test_user_role_is_SALE(user_in_sale_group):
    assert user_in_sale_group.user_role == 'SALE'


def test_user_role_is_SUPPORT(user_in_support_group):
    assert user_in_support_group.user_role == 'SUPPORT'


def test_user_role_error(user_in_two_groups):
    assert user_in_two_groups.user_role == 'ERROR'


def test_user_role_not_admin(user_without_group_not_admin):
    assert user_without_group_not_admin.user_role == 'Inconnu'


def test_user_role_admin(user_is_admin):
    assert user_is_admin.user_role == 'ADMIN'
