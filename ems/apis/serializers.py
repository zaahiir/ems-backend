from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from .models import *


class UserTypeModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserTypeModel
        fields = '__all__'


class StateModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = StateModel
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


class GuardianRelationshipModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = GuardianRelationshipModel
        fields = '__all__'


class DefaultAccountModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = DefaultAccountModel
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
    class Meta:
        model = AumEntryModel
        fields = '__all__'


class CommissionEntryModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = CommissionEntryModel
        fields = '__all__'


class AumYoyGrowthEntryModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = AumYoyGrowthEntryModel
        fields = '__all__'


class IndustryAumEntryModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = IndustryAumEntryModel
        fields = '__all__'


class GstEntryModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = GstEntryModel
        fields = '__all__'


class NavModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = NavModel
        fields = '__all__'


class IssueModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = IssueModel
        fields = '__all__'


class StatementModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = StatementModel
        fields = '__all__'


class CourierModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = CourierModel
        fields = '__all__'


class FormsModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = FormsModel
        fields = '__all__'


class MarketingModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = MarketingModel
        fields = '__all__'


class TaskModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = '__all__'


class EmployeeModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmployeeModel
        fields = '__all__'


# class ClientModelSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = ClientModel
#         fields = '__all__'
#
#
# class ClientFamilyDetailModelSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = ClientFamilyDetailModel
#         fields = '__all__'
#
#
# class ClientChildrenDetailModelSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = ClientChildrenDetailModel
#         fields = '__all__'
#
#
# class ClientPresentAddressModelSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = ClientPresentAddressModel
#         fields = '__all__'
#
#
# class ClientPermanentAddressModelSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = ClientPermanentAddressModel
#         fields = '__all__'
#
#
# class ClientOfficeAddressModelSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = ClientOfficeAddressModel
#         fields = '__all__'
#
#
# class ClientOverseasAddressModelSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = ClientOverseasAddressModel
#         fields = '__all__'
#
#
# class ClientNomineeModelSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = ClientNomineeModel
#         fields = '__all__'
#
#
# class ClientMedicalInsuranceModelSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = ClientMedicalInsuranceModel
#         fields = '__all__'
#
#
# class ClientTermInsuranceModelSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = ClientTermInsuranceModel
#         fields = '__all__'
#
#
# class ClientUploadFileModelSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = ClientUploadFileModel
#         fields = '__all__'
#
#
# class ClientBankModelSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = ClientBankModel
#         fields = '__all__'
#
#
# class ClientTaxModelSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = ClientTaxModel
#         fields = '__all__'
#
#
# class ClientPowerOfAttorneyModelSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = ClientPowerOfAttorneyModel
#         fields = '__all__'
#
