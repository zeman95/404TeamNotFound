# Generated by Django 2.1.1 on 2018-11-06 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TLS', '0003_remove_document_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]