# Generated by Django 3.0.7 on 2020-06-19 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detalji_za_pretragu', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detaljipretrage',
            old_name='naziv',
            new_name='naziv_detalji',
        ),
    ]