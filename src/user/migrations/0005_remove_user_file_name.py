# Generated by Django 4.0.1 on 2022-01-23 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_file_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='file_name',
        ),
    ]
