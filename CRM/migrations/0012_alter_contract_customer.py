# Generated by Django 3.2.9 on 2021-11-03 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0011_alter_eventstatus_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='customer',
            field=models.ForeignKey(help_text='Each contract is related to a customer', on_delete=django.db.models.deletion.CASCADE, related_name='contracts_customer', to='CRM.customer', verbose_name='customer'),
        ),
    ]