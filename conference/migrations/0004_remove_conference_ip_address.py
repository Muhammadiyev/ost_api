# Generated by Django 2.2.7 on 2020-02-19 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0003_conference_ip_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conference',
            name='ip_address',
        ),
    ]