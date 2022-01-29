# Generated by Django 4.0.1 on 2022-01-23 12:17

import django.core.validators
from django.db import migrations, models
import src.base.services


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_managers_remove_user_is_staff_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default=1, upload_to=src.base.services.get_path_upload_avatar, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg'])]),
            preserve_default=False,
        ),
    ]
