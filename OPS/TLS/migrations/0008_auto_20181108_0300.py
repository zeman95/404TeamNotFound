# Generated by Django 2.1.1 on 2018-11-08 03:00

import TLS.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TLS', '0007_auto_20181108_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='file',
            field=models.FileField(upload_to='attachments', validators=[TLS.models.validate_file_extension], verbose_name='Attachment'),
        ),
    ]
