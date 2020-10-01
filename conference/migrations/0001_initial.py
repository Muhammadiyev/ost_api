# Generated by Django 2.2.7 on 2020-10-01 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('when', models.CharField(blank=True, max_length=100)),
                ('timezone', models.CharField(blank=True, max_length=100)),
                ('duration', models.CharField(blank=True, max_length=100, null=True)),
                ('not_limited', models.BooleanField(default=False, verbose_name='not_limited')),
                ('typeconf', models.IntegerField(blank=True, choices=[(1, 'Conference'), (2, 'Vebinar')], default=1, null=True)),
                ('save_conf', models.BooleanField(default=False, verbose_name='save_conference')),
                ('start_time', models.CharField(blank=True, max_length=100)),
                ('protected', models.BooleanField(default=True, verbose_name='protected_conference')),
                ('status', models.BooleanField(default=True, verbose_name='status')),
                ('start_status', models.BooleanField(default=True, verbose_name='start_status')),
                ('room_name', models.CharField(blank=True, max_length=1000000)),
                ('security_room', models.CharField(blank=True, max_length=1000000, null=True)),
                ('waiting_room', models.BooleanField(default=True, verbose_name='waiting_room')),
                ('video_organizer', models.BooleanField(default=True, verbose_name='video_organizer')),
                ('video_participant', models.BooleanField(default=True, verbose_name='video_participant')),
                ('entrance_organizer', models.BooleanField(default=True, verbose_name='entrance_organizer')),
                ('off_participant_volume', models.BooleanField(default=True, verbose_name='off_participant_volume')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='conference_of_user', to=settings.AUTH_USER_MODEL)),
                ('usersofroleofdepartments', models.ManyToManyField(blank=True, related_name='conference_of_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TypeConf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OneToOneConf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, default=0)),
                ('status_call', models.BooleanField(default=True, verbose_name='status_call')),
                ('status', models.BooleanField(default=True, verbose_name='status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator_of_user', to=settings.AUTH_USER_MODEL)),
                ('invited', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invited_of_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ConferenceUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_users', models.IntegerField(blank=True)),
                ('status', models.BooleanField(default=True, verbose_name='status_user')),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conferenceuser_of_conference', to='conference.Conference')),
                ('see_user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='conferenceuser_of_customuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
