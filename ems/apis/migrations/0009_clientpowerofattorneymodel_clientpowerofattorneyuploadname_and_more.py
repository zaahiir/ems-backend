# Generated by Django 5.0.6 on 2024-07-26 05:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0008_rename_clientguardianname_clientnomineemodel_clientnomineeguardianname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientpowerofattorneymodel',
            name='clientPowerOfAttorneyUploadName',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='clientpowerofattorneymodel',
            name='clientPowerOfAttorneyUpload',
            field=models.FileField(blank=True, null=True, upload_to='clientPowerOfAttorneyUpload/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'pdf'])]),
        ),
        migrations.AlterField(
            model_name='clientuploadfilemodel',
            name='clientAadharCard',
            field=models.FileField(blank=True, null=True, upload_to='clientAadharCard/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'pdf'])]),
        ),
        migrations.AlterField(
            model_name='clientuploadfilemodel',
            name='clientBankAccountStatementOrPassbook',
            field=models.FileField(blank=True, null=True, upload_to='clientBankAccountStatementOrPassbook/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'pdf'])]),
        ),
        migrations.AlterField(
            model_name='clientuploadfilemodel',
            name='clientCancelledChequeCopy',
            field=models.FileField(blank=True, null=True, upload_to='clientCancelledChequeCopy/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'pdf'])]),
        ),
        migrations.AlterField(
            model_name='clientuploadfilemodel',
            name='clientChildrenBirthCertificate',
            field=models.FileField(blank=True, null=True, upload_to='clientChildrenBirthCertificate/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'pdf'])]),
        ),
        migrations.AlterField(
            model_name='clientuploadfilemodel',
            name='clientDrivingLicense',
            field=models.FileField(blank=True, null=True, upload_to='clientDrivingLicense/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'pdf'])]),
        ),
        migrations.AlterField(
            model_name='clientuploadfilemodel',
            name='clientForeignAddressProof',
            field=models.FileField(blank=True, null=True, upload_to='clientForeignAddressProof/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'pdf'])]),
        ),
        migrations.AlterField(
            model_name='clientuploadfilemodel',
            name='clientForeignTaxIdentificationProof',
            field=models.FileField(blank=True, null=True, upload_to='clientForeignTaxIdentificationProof/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'pdf'])]),
        ),
        migrations.AlterField(
            model_name='clientuploadfilemodel',
            name='clientPaasPortSizePhoto',
            field=models.FileField(blank=True, null=True, upload_to='clientPaasPortSizePhoto/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'pdf'])]),
        ),
        migrations.AlterField(
            model_name='clientuploadfilemodel',
            name='clientPanCardPhoto',
            field=models.FileField(blank=True, null=True, upload_to='clientPanCardPhoto/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'pdf'])]),
        ),
        migrations.AlterField(
            model_name='clientuploadfilemodel',
            name='clientPassportBackImage',
            field=models.FileField(blank=True, null=True, upload_to='clientPassportBackImage/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'pdf'])]),
        ),
        migrations.AlterField(
            model_name='clientuploadfilemodel',
            name='clientPassportFrontImage',
            field=models.FileField(blank=True, null=True, upload_to='clientPassportFrontImage/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'pdf'])]),
        ),
        migrations.AlterField(
            model_name='clientuploadfilemodel',
            name='clientVoterIDBackImage',
            field=models.FileField(blank=True, null=True, upload_to='clientVoterIDBackImage/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'pdf'])]),
        ),
        migrations.AlterField(
            model_name='clientuploadfilemodel',
            name='clientVoterIDFrontImage',
            field=models.FileField(blank=True, null=True, upload_to='clientVoterIDFrontImage/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'pdf'])]),
        ),
        migrations.AlterField(
            model_name='employeemodel',
            name='employeeFile',
            field=models.FileField(blank=True, null=True, upload_to='employeeFile/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg'])]),
        ),
    ]
