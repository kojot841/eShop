# Generated by Django 3.0.7 on 2020-06-30 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('porudzbine', '0004_auto_20200630_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='porudzbina',
            name='status',
            field=models.CharField(choices=[('kreirana', 'Kreirana'), ('placena', 'Placena'), ('poslata', 'Poslata')], default='kreirana', max_length=120),
        ),
    ]
