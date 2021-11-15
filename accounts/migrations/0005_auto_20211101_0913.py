# Generated by Django 3.2.8 on 2021-11-01 08:13

from django.db import migrations


def create_groups(apps, schema_migration):
    
    from django.apps.registry import Apps, apps as global_apps
    from django.contrib.contenttypes.management import create_contenttypes
    CRM_config = global_apps.get_app_config('CRM')
    create_contenttypes(CRM_config)
    
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    customer_ct = ContentType.objects.get(model="customer")
    contract_ct = ContentType.objects.get(model="contract")
    event_ct = ContentType.objects.get(model="event")

    view_customer = Permission.objects.get_or_create(codename='view_customer', content_type=customer_ct)
    view_contract = Permission.objects.get_or_create(codename='view_contract', content_type=contract_ct)
    view_event = Permission.objects.get_or_create(codename='view_event', content_type=event_ct)

    add_customer = Permission.objects.get_or_create(codename='add_customer', content_type=customer_ct)
    add_contract = Permission.objects.get_or_create(codename='add_contract', content_type=contract_ct)
    add_event = Permission.objects.get_or_create(codename='add_event', content_type=event_ct)

    change_customer = Permission.objects.get_or_create(codename='change_customer', content_type=customer_ct)
    change_contract = Permission.objects.get_or_create(codename='change_contract', content_type=contract_ct)
    change_event = Permission.objects.get_or_create(codename='change_event', content_type=event_ct)

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

    support_permissions = [
        view_customer,
        view_contract,
        view_event,
        change_event,
    ]

    sale = Group(name='sale')
    sale.save()
    sale.permissions.set(sale_permissions)

    support = Group(name='support')
    support.save()
    support.permissions.set(support_permissions)

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_role'),
    ]

    operations = [
        migrations.RunPython(create_groups)
    ]
