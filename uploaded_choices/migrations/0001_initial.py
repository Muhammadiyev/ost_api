# Generated by Django 2.2.7 on 2020-02-18 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=1)),
                ('file', models.FileField(null=True, upload_to='get_random_path')),
                ('type', models.CharField(max_length=1)),
            ],
        ),
    ]