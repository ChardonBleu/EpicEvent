# Generated by Django 3.2.9 on 2021-11-15 12:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, help_text='contract creation datetime is automatically filled in.', verbose_name='Date création contrat')),
                ('datetime_updated', models.DateTimeField(auto_now=True, help_text='contract update datetime is automatically filled in.', verbose_name='Date mise à jour contrat')),
                ('status_sign', models.BooleanField(default=False, help_text='Has to pass on True when contract is signed', verbose_name='Signature contrat')),
                ('amount', models.DecimalField(decimal_places=2, help_text='Contract amount when signed. Float number', max_digits=9, verbose_name='Montant du contrat')),
                ('payment_due', models.DateField(help_text='Payment due. Format: AAAA-MM-JJ', verbose_name='Echéance de paiement')),
            ],
            options={
                'verbose_name_plural': 'Contrats',
                'ordering': ['customer', '-datetime_created'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Each customer has a first name with max 25 caracters.', max_length=25, verbose_name='Prénom client')),
                ('last_name', models.CharField(help_text='Each customer has a last name with max 25 caracters.', max_length=25, verbose_name='Nom de famille client')),
                ('email', models.EmailField(help_text='Each customer has an email with max 100 caracters.', max_length=100, verbose_name='email client')),
                ('phone', models.CharField(blank=True, help_text='Each customer has a phone number with max 20 caracters.', max_length=20, verbose_name='Téléphone fixe client')),
                ('mobile', models.CharField(help_text='Each customer has a mobile phone number with max 20             caracters.', max_length=20, verbose_name='Téléphone mobile client')),
                ('company_name', models.CharField(blank=True, help_text='Company name customer for professional customers with            max 250 caracters.', max_length=250, verbose_name='Company')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, help_text='custumer creation datetime is automatically filled in.', verbose_name='Date création client')),
                ('datetime_updated', models.DateTimeField(auto_now=True, help_text='custumer update datetime is automatically filled in.', verbose_name='Date mise à jour client')),
            ],
            options={
                'verbose_name_plural': 'Clients',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='EventStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(help_text='For event status choice. Three choices            possibles: En préparation, En cours, Terminé', max_length=250, verbose_name='Status évènement')),
            ],
            options={
                'verbose_name_plural': 'Status évènements',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, help_text='event creation datetime is automatically filled in.', verbose_name='Date création évènement')),
                ('datetime_updated', models.DateTimeField(auto_now=True, help_text='event update datetime is automatically filled in.', verbose_name='Date mise à jour évènement')),
                ('attendees', models.IntegerField(blank=True, help_text='number of attendees. Must be positive integer', null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Nombre convives')),
                ('event_date', models.DateField(blank=True, help_text='Date event. Format: AAAA-MM-JJ', null=True, verbose_name="Date de l'évènement")),
                ('notes', models.TextField(blank=True, help_text='Notes and organisation details.', verbose_name="Notes et détails d'organisation")),
                ('customer', models.ForeignKey(help_text='Each event is related to a custumer', on_delete=django.db.models.deletion.CASCADE, related_name='events_customer', to='CRM.customer', verbose_name='customer')),
                ('status', models.ForeignKey(default=1, help_text="Each event has a status: '1: En préparation',            '2: En cours' or '3: Terminé'", on_delete=django.db.models.deletion.CASCADE, related_name='status_events', to='CRM.eventstatus', verbose_name='status évènement')),
            ],
            options={
                'verbose_name_plural': 'Evènements',
                'ordering': ['status', 'event_date'],
            },
        ),
    ]
