# Generated by Django 2.1.1 on 2018-11-08 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TLS', '0010_auto_20181108_0425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='message',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TLS.Message', verbose_name='Message'),
        ),
        migrations.AlterField(
            model_name='message',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]