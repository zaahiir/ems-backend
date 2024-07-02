# Generated by Django 5.0.6 on 2024-06-25 05:28

import django_countries.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0007_remove_amcentrymodel_amcemail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statemodel',
            name='country',
        ),
        migrations.AlterField(
            model_name='arnentrymodel',
            name='arnCountry',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='amcentrymodel',
            name='amcCountry',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
        migrations.DeleteModel(
            name='CountryModel',
        ),
    ]
