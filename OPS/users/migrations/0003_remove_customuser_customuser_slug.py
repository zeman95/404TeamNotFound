# Generated by Django 2.1.1 on 2018-11-08 04:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_customuser_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='CustomUser_slug',
        ),
    ]