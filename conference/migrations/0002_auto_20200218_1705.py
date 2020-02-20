# Generated by Django 2.2.7 on 2020-02-18 12:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('conference', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='conferenceuser',
            name='see_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='see_user_of_customuser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='conference',
            name='typeconf',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conference_of_type', to='conference.TypeConf'),
        ),
        migrations.AddField(
            model_name='conference',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conference_of_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='conference',
            name='usersofroleofdepartments',
            field=models.ManyToManyField(blank=True, related_name='conference_of_users', to=settings.AUTH_USER_MODEL),
        ),
    ]