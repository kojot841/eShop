# Generated by Django 3.0.7 on 2020-06-22 10:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proizvodi', '0002_remove_proizvodi_kratakopis'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Placanje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ukupno', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('izmena', models.DateTimeField(auto_now=True)),
                ('vreme', models.DateTimeField(auto_now_add=True)),
                ('korisnik', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('proizvodi', models.ManyToManyField(blank=True, to='proizvodi.Proizvodi')),
            ],
        ),
    ]
