# Generated by Django 5.0.7 on 2024-10-17 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0027_activitylog'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitylog',
            name='previous_data',
            field=models.JSONField(null=True),
        ),
    ]
