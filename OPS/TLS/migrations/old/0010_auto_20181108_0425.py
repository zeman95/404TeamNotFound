# Generated by Django 2.1.1 on 2018-11-08 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TLS', '0009_auto_20181108_0325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='file',
            field=models.FileField(upload_to='documents', verbose_name='Attachment'),
        ),
    ]