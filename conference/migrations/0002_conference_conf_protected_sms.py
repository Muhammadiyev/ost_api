# Generated by Django 2.2.7 on 2020-12-12 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='conf_protected_sms',
            field=models.BooleanField(default=True, null=True, verbose_name='conf_protected_sms'),
        ),
    ]