# Generated by Django 5.0.7 on 2024-10-05 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0025_alter_arnentrymodel_arngstno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arnentrymodel',
            name='arnGstNo',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
