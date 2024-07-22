from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from django.core.validators import FileExtensionValidator

from .models import *


class UserTypeModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserTypeModel
        fields = '__all__'


class StateModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = StateModel
        fields = '__all__'


class ModeModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ModeModel
        fields = '__all__'


class IssueTypeModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = IssueTypeModel
        fields = '__all__'


class FormTypeModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = FormTypeModel
        fields = '__all__'


class GstTypeModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = GstTypeModel
        fields = '__all__'


class GenderModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = GenderModel
        fields = '__all__'


class MaritalStatusModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = MaritalStatusModel
        fields = '__all__'


class PoliticallyExposedPersonModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = PoliticallyExposedPersonModel
        fields = '__all__'


class BankNameModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = BankNameModel
        fields = '__all__'


class RelationshipModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = RelationshipModel
        fields = '__all__'


class AccountTypeModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = AccountTypeModel
        fields = '__all__'


class AccountPreferenceModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = AccountPreferenceModel
        fields = '__all__'


class ArnEntryModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ArnEntryModel
        fields = '__all__'


class AmcEntryModelSerializers(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = AmcEntryModel
        fields = '__all__'


class AumEntryModelSerializers(serializers.ModelSerializer):
    aumArnNumber = serializers.PrimaryKeyRelatedField(queryset=ArnEntryModel.objects.all())
    aumAmcAbbreviation = serializers.PrimaryKeyRelatedField(queryset=AmcEntryModel.objects.all())

    class Meta:
        model = AumEntryModel
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['aumArnNumber'] = instance.aumArnNumber.arnNumber if instance.aumArnNumber else None
        representation[
            'aumAmcAbbreviation'] = instance.aumAmcAbbreviation.amcAbbreviation if instance.aumAmcAbbreviation else None
        return representation


class CommissionEntryModelSerializers(serializers.ModelSerializer):
    commissionArnNumber = serializers.PrimaryKeyRelatedField(queryset=ArnEntryModel.objects.all())
    commissionAmcAbbreviation = serializers.PrimaryKeyRelatedField(queryset=AmcEntryModel.objects.all())

    class Meta:
        model = CommissionEntryModel
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation[
            'commissionArnNumber'] = instance.commissionArnNumber.arnNumber if instance.commissionArnNumber else None
        representation[
            'commissionAmcAbbreviation'] = instance.commissionAmcAbbreviation.amcAbbreviation if instance.commissionAmcAbbreviation else None
        return representation


class AumYoyGrowthEntryModelSerializers(serializers.ModelSerializer):
    aumYoyGrowthAmcAbbreviation = serializers.PrimaryKeyRelatedField(queryset=AmcEntryModel.objects.all())

    class Meta:
        model = AumYoyGrowthEntryModel
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation[
            'aumYoyGrowthAmcAbbreviation'] = instance.aumYoyGrowthAmcAbbreviation.amcAbbreviation if instance.aumYoyGrowthAmcAbbreviation else None
        return representation


class IndustryAumEntryModelSerializers(serializers.ModelSerializer):
    industryAumMode = serializers.PrimaryKeyRelatedField(queryset=ModeModel.objects.all())

    class Meta:
        model = IndustryAumEntryModel
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['industryAumMode'] = instance.industryAumMode.modeName if instance.industryAumMode else None
        return representation


class GstEntryModelSerializers(serializers.ModelSerializer):
    gstAmcAbbreviation = serializers.PrimaryKeyRelatedField(queryset=AmcEntryModel.objects.all())

    class Meta:
        model = GstEntryModel
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation[
            'gstAmcAbbreviation'] = instance.gstAmcAbbreviation.amcAbbreviation if instance.gstAmcAbbreviation else None
        return representation


class NavModelSerializers(serializers.ModelSerializer):
    navAmcName = serializers.PrimaryKeyRelatedField(queryset=AmcEntryModel.objects.all())

    class Meta:
        model = NavModel
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['navAmcName'] = instance.navAmcName.amcAbbreviation if instance.navAmcName else None
        return representation


class IssueModelSerializers(serializers.ModelSerializer):
    issueType = serializers.PrimaryKeyRelatedField(queryset=IssueTypeModel.objects.all())

    class Meta:
        model = IssueModel
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['issueType'] = instance.issueType.issueTypeName if instance.issueType else None
        return representation


class StatementModelSerializers(serializers.ModelSerializer):
    statementAmcName = serializers.PrimaryKeyRelatedField(queryset=AmcEntryModel.objects.all())

    class Meta:
        model = StatementModel
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation[
            'statementAmcName'] = instance.statementAmcName.amcAbbreviation if instance.statementAmcName else None
        return representation


class CourierFileModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = CourierFileModel
        fields = ('id', 'courierFile')


class CourierModelSerializers(serializers.ModelSerializer):
    courierFile = serializers.ListField(
        child=serializers.FileField(
            max_length=100000,
            allow_empty_file=False,
            use_url=False,
            validators=[FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'xls', 'xlsx', 'csv', 'txt']
            )]
        ),
        write_only=True,
        required=False
    )
    files = CourierFileModelSerializers(many=True, read_only=True, source='courier')

    class Meta:
        model = CourierModel
        fields = '__all__'

    def create(self, validated_data):
        files_data = validated_data.pop('courierFile', None)
        courier = CourierModel.objects.create(**validated_data)
        if files_data:
            for file_data in files_data:
                CourierFileModel.objects.create(courier=courier, courierFile=file_data)
        return courier

    def update(self, instance, validated_data):
        files_data = validated_data.pop('courierFile', None)
        instance = super().update(instance, validated_data)
        if files_data:
            for file_data in files_data:
                CourierFileModel.objects.create(courier=instance, courierFile=file_data)
        return instance


class FormsModelSerializers(serializers.ModelSerializer):
    formsAmcName = serializers.PrimaryKeyRelatedField(queryset=AmcEntryModel.objects.all())
    formsType = serializers.PrimaryKeyRelatedField(queryset=FormTypeModel.objects.all())
    formsFile = serializers.FileField(
        allow_empty_file=True,
        use_url=False,
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=[
            'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'xls', 'xlsx', 'csv', 'txt'
        ])]
    )

    class Meta:
        model = FormsModel
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['formsAmcName'] = instance.formsAmcName.amcAbbreviation if instance.formsAmcName else None
        representation['formsType'] = instance.formsType.formTypeName if instance.formsType else None
        if instance.formsFile:
            representation['formsFile'] = instance.formsFile.url
        return representation


class MarketingModelSerializers(serializers.ModelSerializer):
    marketingAmcName = serializers.PrimaryKeyRelatedField(queryset=AmcEntryModel.objects.all())
    marketingFile = serializers.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'xls', 'xlsx', 'csv', 'txt'])],
        required=False
    )

    class Meta:
        model = MarketingModel
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['marketingAmcName'] = instance.marketingAmcName.amcAbbreviation if instance.marketingAmcName else None
        if instance.marketingFile:
            representation['marketingFile'] = instance.marketingFile.url
        return representation


class TaskModelSerializers(serializers.ModelSerializer):
    taskClient = serializers.PrimaryKeyRelatedField(queryset=ClientModel.objects.all())

    class Meta:
        model = TaskModel
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['taskClient'] = instance.taskClient.clientName if instance.taskClient else None
        return representation


class EmployeeModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmployeeModel
        fields = '__all__'


class ClientModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientModel
        fields = '__all__'


class ClientFamilyDetailModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientFamilyDetailModel
        fields = '__all__'


class ClientChildrenDetailModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientChildrenDetailModel
        fields = '__all__'


class ClientPresentAddressModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientPresentAddressModel
        fields = '__all__'


class ClientPermanentAddressModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientPermanentAddressModel
        fields = '__all__'


class ClientOfficeAddressModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientOfficeAddressModel
        fields = '__all__'


class ClientOverseasAddressModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientOverseasAddressModel
        fields = '__all__'


class ClientNomineeModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientNomineeModel
        fields = '__all__'


class ClientInsuranceModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientInsuranceModel
        fields = '__all__'


class ClientMedicalInsuranceModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientMedicalInsuranceModel
        fields = '__all__'


class ClientTermInsuranceModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientTermInsuranceModel
        fields = '__all__'


class ClientUploadFileModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientUploadFileModel
        fields = '__all__'


class ClientBankModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientBankModel
        fields = '__all__'


class ClientTaxModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientTaxModel
        fields = '__all__'


class ClientPowerOfAttorneyModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientPowerOfAttorneyModel
        fields = '__all__'


class ClientGuardianModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientGuardianModel
        fields = '__all__'
