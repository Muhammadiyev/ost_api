# Generated by Django 2.2.7 on 2020-02-22 12:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(blank=True, max_length=100, null=True)),
                ('discussion', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('when', models.DateTimeField(auto_now_add=True)),
                ('duration', models.DurationField()),
                ('save_conf', models.BooleanField(default=False, verbose_name='save_conference')),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('protected', models.BooleanField(default=True, verbose_name='protected_conference')),
                ('status', models.BooleanField(default=True, verbose_name='public_conference')),
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
            name='ConferenceUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_users', models.IntegerField(blank=True)),
                ('status', models.BooleanField(default=True, verbose_name='status_user')),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='confuser_of_conference', to='conference.Conference')),
            ],
        ),
    ]
