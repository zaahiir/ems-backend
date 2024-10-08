# Generated by Django 5.0.7 on 2024-09-27 05:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0014_alter_marketingmodel_marketingtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('countryName', models.CharField(blank=True, max_length=200, null=True)),
                ('countryCode', models.CharField(blank=True, max_length=55, null=True)),
                ('dailCode', models.CharField(blank=True, max_length=10, null=True)),
                ('hideStatus', models.IntegerField(default=0)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='statemodel',
            name='stateCountry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stateCountry', to='apis.countrymodel'),
        ),
    ]
