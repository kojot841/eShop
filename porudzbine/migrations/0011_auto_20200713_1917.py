# Generated by Django 3.0.7 on 2020-07-13 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('porudzbine', '0010_auto_20200713_1912'),
    ]

    operations = [
        migrations.RenameField(
            model_name='porudzbina',
            old_name='broj_placanja',
            new_name='placanje_narudzbina',
        ),
    ]