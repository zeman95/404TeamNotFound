# Generated by Django 2.1.1 on 2018-11-06 03:46

import TLS.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TLS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(null=True, upload_to=TLS.models.user_directory_path, validators=[TLS.models.validate_file_extension]),
        ),
    ]
