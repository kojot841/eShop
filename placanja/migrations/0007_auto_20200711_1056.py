# Generated by Django 3.0.7 on 2020-07-11 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proizvodi', '0002_remove_proizvodi_kratakopis'),
        ('placanja', '0006_auto_20200624_1154'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('proizvod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proizvodi.Proizvodi')),
            ],
        ),
        migrations.AddField(
            model_name='placanje',
            name='item',
            field=models.ManyToManyField(blank=True, null=True, to='placanja.CartItems'),
        ),
    ]
