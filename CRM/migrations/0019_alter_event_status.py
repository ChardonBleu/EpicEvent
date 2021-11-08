# Generated by Django 3.2.9 on 2021-11-08 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0018_remove_event_event_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.ForeignKey(default=1, help_text="Each event has a status: '1: En préparation',            '2: En cours' or '3: Terminé'", on_delete=django.db.models.deletion.CASCADE, related_name='status_events', to='CRM.eventstatus', verbose_name='status évènement'),
        ),
    ]