# Generated by Django 5.0.7 on 2024-09-19 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0008_issuemodel_issuedailyentry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issuemodel',
            name='issueDailyEntry',
        ),
    ]
