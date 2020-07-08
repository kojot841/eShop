# Generated by Django 3.0.7 on 2020-06-30 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('porudzbine', '0005_porudzbina_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='porudzbina',
            old_name='placanje',
            new_name='placanje_narudzbina',
        ),
        migrations.AlterField(
            model_name='porudzbina',
            name='status',
            field=models.CharField(choices=[('created', 'Kreirana'), ('paid', 'Placena'), ('shipped', 'Poslata')], default='created', max_length=120),
        ),
    ]
