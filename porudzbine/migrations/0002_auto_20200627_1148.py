# Generated by Django 3.0.7 on 2020-06-27 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('placanja', '0006_auto_20200624_1154'),
        ('porudzbine', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='porudzbina',
            name='id_porudzbine',
            field=models.CharField(blank=True, max_length=240),
        ),
        migrations.AddField(
            model_name='porudzbina',
            name='narudzbina',
            field=models.ForeignKey(default=12345, on_delete=django.db.models.deletion.CASCADE, to='placanja.Placanje'),
            preserve_default=False,
        ),
    ]
