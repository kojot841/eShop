# Generated by Django 3.0.7 on 2020-07-11 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placanja', '0007_auto_20200711_1056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='placanje',
            name='item',
        ),
        migrations.DeleteModel(
            name='CartItems',
        ),
    ]