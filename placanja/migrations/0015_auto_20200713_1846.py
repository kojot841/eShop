# Generated by Django 3.0.7 on 2020-07-13 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placanja', '0014_auto_20200712_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placanje',
            name='ukupno',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
    ]