# Generated by Django 3.0.7 on 2020-06-24 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placanja', '0003_auto_20200622_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='placanje',
            name='postarina',
            field=models.PositiveIntegerField(default=250, null=True),
        ),
    ]
