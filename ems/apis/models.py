from django.core.validators import FileExtensionValidator
from django_countries.fields import CountryField
from django.db import models
from month.models import MonthField


# Create your models here.

# Start of Master
class UserTypeModel(models.Model):
    id = models.AutoField(primary_key=True)
    userTypeName = models.CharField(max_length=200, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class StateModel(models.Model):
    id = models.AutoField(primary_key=True)
    stateName = models.CharField(max_length=200, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class GenderModel(models.Model):
    id = models.AutoField(primary_key=True)
    genderName = models.CharField(max_length=200, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class MaritalStatusModel(models.Model):
    id = models.AutoField(primary_key=True)
    maritalStatusName = models.CharField(max_length=200, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class PoliticallyExposedPersonModel(models.Model):
    id = models.AutoField(primary_key=True)
    politicallyExposedPersonName = models.CharField(max_length=200, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class BankNameModel(models.Model):
    id = models.AutoField(primary_key=True)
    bankName = models.CharField(max_length=200, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class GuardianRelationshipModel(models.Model):
    id = models.AutoField(primary_key=True)
    guardianRelationship = models.CharField(max_length=200, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class DefaultAccountModel(models.Model):
    id = models.AutoField(primary_key=True)
    defaultAccount = models.CharField(max_length=200, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


# End of Master


class ArnEntryModel(models.Model):
    id = models.AutoField(primary_key=True)
    arnNumber = models.CharField(max_length=200, null=True, blank=True)
    arnName = models.CharField(max_length=200, null=True, blank=True)
    arnMobile = models.CharField(max_length=200, null=True, blank=True)
    arnAddress = models.CharField(max_length=500, null=True, blank=True)
    arnState = models.ForeignKey(StateModel, on_delete=models.CASCADE, related_name="arnState", null=True, blank=True)
    arnCountry = CountryField(blank_label='(select country)', null=True, blank=True)
    arnPinCode = models.IntegerField(null=True, blank=True)
    arnEmail = models.EmailField(unique=True)
    arnEvin = models.CharField(max_length=200, null=True, blank=True)
    arnGstNo = models.CharField(max_length=50, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class AmcEntryModel(models.Model):
    id = models.AutoField(primary_key=True)
    amcAbbreviation = models.CharField(max_length=200, null=True, blank=True)
    amcName = models.CharField(max_length=200, null=True, blank=True)
    amcMobile = models.CharField(max_length=200, null=True, blank=True)
    amcAddress = models.CharField(max_length=500, null=True, blank=True)
    amcState = models.ForeignKey(StateModel, on_delete=models.CASCADE, related_name="amcState", null=True, blank=True)
    amcCountry = CountryField(blank_label='(select country)', null=True, blank=True)
    amcPinCode = models.IntegerField(null=True, blank=True)
    amcGstNo = models.CharField(max_length=50, null=True, blank=True)
    amcGstType = models.CharField(max_length=200, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class AumEntryModel(models.Model):
    id = models.AutoField(primary_key=True)
    aumArnNumber = models.ForeignKey(ArnEntryModel, on_delete=models.CASCADE, related_name="aumArnNumber", null=True,
                                     blank=True)
    aumAmcAbbreviation = models.ForeignKey(AmcEntryModel, on_delete=models.CASCADE, related_name="aumAmcAbbreviation",
                                           null=True, blank=True)
    aumInvoiceNumber = models.CharField(max_length=200, null=True, blank=True)
    aumAmount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    aumMonth = models.CharField(max_length=7, help_text="Format: YYYY-MM")
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class CommissionEntryModel(models.Model):
    id = models.AutoField(primary_key=True)
    commissionArnNumber = models.ForeignKey(ArnEntryModel, on_delete=models.CASCADE, related_name="commissionArnNumber",
                                            null=True, blank=True)
    commissionAmcAbbreviation = models.ForeignKey(AmcEntryModel, on_delete=models.CASCADE,
                                                  related_name="commissionAmcAbbreviation", null=True, blank=True)
    commissionAmount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    commissionMonth = models.CharField(max_length=7, help_text="Format: YYYY-MM")
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class AumYoyGrowthEntryModel(models.Model):
    id = models.AutoField(primary_key=True)
    aumYoyGrowthAmcAbbreviation = models.ForeignKey(AmcEntryModel, on_delete=models.CASCADE,
                                                    related_name="aumYoyGrowthAmcAbbreviation", null=True, blank=True)
    aumYoyGrowthAmount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    aumYoyGrowthDate = models.DateField(null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class IndustryAumEntryModel(models.Model):
    id = models.AutoField(primary_key=True)
    industryName = models.CharField(max_length=200, null=True, blank=True)
    industryAumDate = models.DateField(null=True, blank=True)
    industryAumAmount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    industryAumSiplone = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class GstEntryModel(models.Model):
    id = models.AutoField(primary_key=True)
    gstInvoiceDate = models.DateField(null=True, blank=True)
    gstInvoiceNumber = models.CharField(max_length=200, null=True, blank=True)
    gstAmcAbbreviation = models.ForeignKey(AmcEntryModel, on_delete=models.CASCADE, related_name="gstAmcAbbreviation",
                                           null=True, blank=True)
    gstTotalValue = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gstTaxableValue = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gstIGst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gstSGst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gstCGst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class NavModel(models.Model):
    id = models.AutoField(primary_key=True)
    navAmcName = models.ForeignKey(AmcEntryModel, on_delete=models.CASCADE, related_name="navAmcName", null=True,
                                   blank=True)
    navFundName = models.CharField(max_length=200, null=True, blank=True)
    nav = models.CharField(max_length=200, null=True, blank=True)
    navDate = models.DateField(null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class IssueModel(models.Model):
    id = models.AutoField(primary_key=True)
    issueName = models.CharField(max_length=200, null=True, blank=True)
    issueType = models.CharField(max_length=200, null=True, blank=True)
    issueDate = models.DateField(null=True, blank=True)
    issueResolutionDate = models.DateField(null=True, blank=True)
    issueDescription = models.CharField(max_length=2500, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class StatementModel(models.Model):
    id = models.AutoField(primary_key=True)
    statementDate = models.DateField(null=True, blank=True)
    statementInvestorName = models.CharField(max_length=200, null=True, blank=True)
    statementInvestorPanNo = models.CharField(max_length=200, null=True, blank=True)
    statementInvestmentDate = models.DateField(null=True, blank=True)
    statementAmcName = models.ForeignKey(AmcEntryModel, on_delete=models.CASCADE, related_name="statementAmcName",
                                         null=True, blank=True)
    statementFundName = models.CharField(max_length=200, null=True, blank=True)
    statementCostOfInvestment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    statementCurrentValue = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    statementSipDate = models.DateField(null=True, blank=True)
    statementSipAmount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    statementSwpAmount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    statementSipBankName = models.CharField(max_length=200, null=True, blank=True)
    statementSipBankAccountType = models.CharField(max_length=200, null=True, blank=True)
    statementSipBankAccountLastFourDigit = models.IntegerField(null=True, blank=True)
    statementPrimaryBankName = models.CharField(max_length=200, null=True, blank=True)
    statementPrimaryBankAccountType = models.CharField(max_length=200, null=True, blank=True)
    statementPrimaryBankAccountLastFourDigit = models.IntegerField(null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class CourierModel(models.Model):
    id = models.AutoField(primary_key=True)
    courierClientName = models.CharField(max_length=200, null=True, blank=True)
    courierClientAddress = models.CharField(max_length=500, null=True, blank=True)
    courierMobileNumber = models.CharField(max_length=200, null=True, blank=True)
    courierEmail = models.EmailField(unique=True)
    courierFile = models.FileField(upload_to="courierFile/", null=True, blank=True,
                                   validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class FormsModel(models.Model):
    id = models.AutoField(primary_key=True)
    formsAmcName = models.ForeignKey(AmcEntryModel, on_delete=models.CASCADE, related_name="formsAmcName", null=True,
                                     blank=True)
    formsType = models.CharField(max_length=500, null=True, blank=True)
    formsDescription = models.CharField(max_length=2500, null=True, blank=True)
    formsFile = models.FileField(upload_to="formsFile/", null=True, blank=True,
                                 validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class MarketingModel(models.Model):
    id = models.AutoField(primary_key=True)
    marketingAmcName = models.ForeignKey(AmcEntryModel, on_delete=models.CASCADE, related_name="marketingAmcName",
                                         null=True, blank=True)
    marketingType = models.CharField(max_length=500, null=True, blank=True)
    marketingDescription = models.CharField(max_length=2500, null=True, blank=True)
    marketingFile = models.FileField(upload_to="marketingFile/", null=True, blank=True,
                                     validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class TaskModel(models.Model):
    id = models.AutoField(primary_key=True)
    taskTitle = models.CharField(max_length=500, null=True, blank=True)
    taskClient = models.CharField(max_length=500, null=True, blank=True)
    taskDate = models.DateField(null=True, blank=True)
    taskTime = models.TimeField(null=True, blank=True)
    taskLatitude = models.CharField(max_length=500, null=True, blank=True)
    taskLongtitude = models.CharField(max_length=500, null=True, blank=True)
    taskDescription = models.CharField(max_length=2500, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class EmployeeModel(models.Model):
    id = models.AutoField(primary_key=True)
    employeeName = models.CharField(max_length=500, null=True, blank=True)
    employeeEmail = models.EmailField(unique=True)
    employeePhone = models.CharField(max_length=500, null=True, blank=True)
    employeePassword = models.CharField(max_length=500, null=True, blank=True)
    employeeAddress = models.CharField(max_length=2500, null=True, blank=True)
    employeeOtherDetail = models.CharField(max_length=2500, null=True, blank=True)
    employeeFile = models.FileField(upload_to="employeeFile/", null=True, blank=True,
                                               validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    employeeUserType = models.ForeignKey(UserTypeModel, on_delete=models.CASCADE, related_name="employeeUserType", null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class ClientModel(models.Model):
    id = models.AutoField(primary_key=True)
    clientName = models.CharField(max_length=500, null=True, blank=True)
    clientEmail = models.EmailField(unique=True)
    clientPhone = models.CharField(max_length=500, null=True, blank=True)
    clientAlternatePhone = models.CharField(max_length=500, null=True, blank=True)
    clientPanNo = models.CharField(max_length=500, null=True, blank=True, unique=True)
    clientKycNo = models.CharField(max_length=500, null=True, blank=True, unique=True)
    clientAadharNo = models.CharField(max_length=500, null=True, blank=True, unique=True)
    clientVoterId = models.CharField(max_length=500, null=True, blank=True, unique=True)
    clientDrivingLicenseNo = models.CharField(max_length=500, null=True, blank=True, unique=True)
    clientDrivingLicenseExpiryDate = models.DateField(null=True, blank=True)
    clientPassportNo = models.CharField(max_length=500, null=True, blank=True, unique=True)
    clientPassportExpiryDate = models.DateField(null=True, blank=True)
    clientCentralGovtId = models.CharField(max_length=500, null=True, blank=True)
    clientCentralGovtIdNo = models.CharField(max_length=500, null=True, blank=True)
    clientBloodGroup = models.CharField(max_length=500, null=True, blank=True)
    clientDateOfBirth = models.DateField(null=True, blank=True)
    clientGender = models.ForeignKey(GenderModel, on_delete=models.CASCADE, related_name="clientGender", null=True, blank=True)
    clientMaritalStatus = models.ForeignKey(MaritalStatusModel, on_delete=models.CASCADE, related_name="clientMaritalStatus", null=True, blank=True)
    clientAnniversaryDate = models.DateField(null=True, blank=True)
    clientCountryOfBirth = CountryField(blank_label='(select country)', null=True, blank=True)
    clientPlaceOfBirth = models.CharField(max_length=500, null=True, blank=True)
    clientCitizenship = models.CharField(max_length=500, null=True, blank=True)
    clientResidentialStatus = models.CharField(max_length=500, null=True, blank=True)
    clientOccupation = models.CharField(max_length=500, null=True, blank=True)
    clientAnnualIncome = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    clientPoliticallyExposed = models.ForeignKey(PoliticallyExposedPersonModel, on_delete=models.CASCADE, related_name="clientPoliticallyExposed", null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class ClientFamilyDetailModel(models.Model):
    id = models.AutoField(primary_key=True)
    clientFamilyDetailId = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name="clientFamilyDetailId", null=True, blank=True)
    clientFatherName = models.CharField(max_length=500, null=True, blank=True)
    clientMotherName = models.CharField(max_length=500, null=True, blank=True)
    clientSpouseName = models.CharField(max_length=500, null=True, blank=True)
    clientSpouseBirthDate = models.DateField(null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class ClientChildrenDetailModel(models.Model):
    id = models.AutoField(primary_key=True)
    clientChildrenId = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name="clientChildrenId", null=True, blank=True)
    clientChildrenName = models.CharField(max_length=500, null=True, blank=True)
    clientChildrenBirthDate = models.DateField(null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class ClientPresentAddressModel(models.Model):
    id = models.AutoField(primary_key=True)
    clientPresentAddressId = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name="clientPresentAddressId", null=True, blank=True)
    clientPresentAddress = models.CharField(max_length=500, null=True, blank=True)
    clientPresentLandmark = models.CharField(max_length=500, null=True, blank=True)
    clientPresentCity = models.CharField(max_length=500, null=True, blank=True)
    clientPresentDistrict = models.CharField(max_length=500, null=True, blank=True)
    clientPresentState = models.ForeignKey(StateModel, on_delete=models.CASCADE, related_name="clientPresentState", null=True, blank=True)
    clientPresentPincode = models.IntegerField(max_length=6, null=True, blank=True)
    clientPresentCountry = CountryField(blank_label='(select country)', null=True, blank=True)
    clientPresentMobile = models.CharField(max_length=500, null=True, blank=True)
    clientPresentLandline = models.CharField(max_length=500, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class ClientPermanentAddressModel(models.Model):
    id = models.AutoField(primary_key=True)
    clientPermanentAddressId = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name="clientPermanentAddressId", null=True, blank=True)
    clientPermanentAddress = models.CharField(max_length=500, null=True, blank=True)
    clientPermanentLandmark = models.CharField(max_length=500, null=True, blank=True)
    clientPermanentCity = models.CharField(max_length=500, null=True, blank=True)
    clientPermanentDistrict = models.CharField(max_length=500, null=True, blank=True)
    clientPermanentState = models.ForeignKey(StateModel, on_delete=models.CASCADE, related_name="clientPermanentState", null=True, blank=True)
    clientPermanentPincode = models.IntegerField(max_length=6, null=True, blank=True)
    clientPermanentCountry = CountryField(blank_label='(select country)', null=True, blank=True)
    clientPermanentMobile = models.CharField(max_length=500, null=True, blank=True)
    clientPermanentLandline = models.CharField(max_length=500, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class ClientOfficeAddressModel(models.Model):
    id = models.AutoField(primary_key=True)
    clientOfficeAddressId = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name="clientOfficeAddressId", null=True, blank=True)
    clientOfficeAddress = models.CharField(max_length=500, null=True, blank=True)
    clientOfficeLandline = models.CharField(max_length=500, null=True, blank=True)
    clientOfficeCity = models.CharField(max_length=500, null=True, blank=True)
    clientOfficeMobile = models.CharField(max_length=500, null=True, blank=True)
    clientOfficeState = models.ForeignKey(StateModel, on_delete=models.CASCADE, related_name="clientOfficeState", null=True, blank=True)
    clientOfficePincode = models.IntegerField(max_length=6, null=True, blank=True)
    clientOfficeCountry = CountryField(blank_label='(select country)', null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class ClientOverseasAddressModel(models.Model):
    id = models.AutoField(primary_key=True)
    clientOverseasAddressId = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name="clientOverseasAddressId", null=True, blank=True)
    clientOverseasAddress = models.CharField(max_length=500, null=True, blank=True)
    clientOverseasLandline = models.CharField(max_length=500, null=True, blank=True)
    clientOverseasCity = models.CharField(max_length=500, null=True, blank=True)
    clientOverseasMobile = models.CharField(max_length=500, null=True, blank=True)
    clientOverseasState = models.ForeignKey(StateModel, on_delete=models.CASCADE, related_name="clientOverseasState", null=True, blank=True)
    clientOverseasPincode = models.IntegerField(max_length=6, null=True, blank=True)
    clientOverseasCountry = CountryField(blank_label='(select country)', null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class ClientNomineeModel(models.Model):
    id = models.AutoField(primary_key=True)
    clientGuardianId = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name="clientGuardianId", null=True, blank=True)
    clientGuardianName = models.CharField(max_length=500, null=True, blank=True)
    clientGuardianRelation = models.ForeignKey(GuardianRelationshipModel, on_delete=models.CASCADE, related_name="clientGuardianRelation", null=True, blank=True)
    clientGuardianPanNo = models.CharField(max_length=500, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class ClientInsuranceModel(models.Model):
    id = models.AutoField(primary_key=True)
    clientInsuranceId = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name="clientInsuranceId", null=True, blank=True)
    clientInsurancePolicyNumber = models.CharField(max_length=500, null=True, blank=True)
    clientInsurancePolicyName = models.CharField(max_length=500, null=True, blank=True)
    clientInsurancePolicyCompanyName = models.CharField(max_length=500, null=True, blank=True)
    clientInsurancePolicyTerm = models.CharField(max_length=500, null=True, blank=True)
    clientInsurancePolicyMaturityAmount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    clientInsurancePolicyPaymentPerInstallment = models.CharField(max_length=500, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class ClientMedicalInsuranceModel(models.Model):
    id = models.AutoField(primary_key=True)
    clientMedicalInsuranceId = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name="clientMedicalInsuranceId", null=True, blank=True)
    clientMedicalInsurancePolicyNumber = models.CharField(max_length=500, null=True, blank=True)
    clientMedicalInsurancePolicyName = models.CharField(max_length=500, null=True, blank=True)
    clientMedicalInsurancePolicyCompanyName = models.CharField(max_length=500, null=True, blank=True)
    clientMedicalInsurancePolicyTerm = models.CharField(max_length=500, null=True, blank=True)
    clientMedicalInsurancePolicyMaturityAmount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    clientMedicalInsurancePolicyPaymentPerInstallment = models.CharField(max_length=500, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class ClientTermInsuranceModel(models.Model):
    id = models.AutoField(primary_key=True)
    clientTermInsuranceId = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name="clientTermInsuranceId", null=True, blank=True)
    clientTermInsurancePolicyNumber = models.CharField(max_length=500, null=True, blank=True)
    clientTermInsurancePolicyName = models.CharField(max_length=500, null=True, blank=True)
    clientTermInsurancePolicyCompanyName = models.CharField(max_length=500, null=True, blank=True)
    clientTermInsurancePolicyTerm = models.CharField(max_length=500, null=True, blank=True)
    clientTermInsurancePolicyMaturityAmount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    clientTermInsurancePolicyPaymentPerInstallment = models.CharField(max_length=500, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class ClientUploadFileModel(models.Model):
    id = models.AutoField(primary_key=True)
    clientUploadFileId = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name="clientUploadFileId", null=True, blank=True)
    clientPaasPortSizePhoto = models.FileField(upload_to="clientPaasPortSizePhoto/", null=True, blank=True,
                                               validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    clientPanCardPhoto = models.FileField(upload_to="clientPanCardPhoto/", null=True, blank=True,
                                               validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    clientAadharCard = models.FileField(upload_to="clientAadharCard/", null=True, blank=True,
                                               validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    clientDrivingLicense = models.FileField(upload_to="clientDrivingLicense/", null=True, blank=True,
                                               validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    clientVoterIDFrontImage = models.FileField(upload_to="clientVoterIDFrontImage/", null=True, blank=True,
                                               validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    clientVoterIDBackImage = models.FileField(upload_to="clientVoterIDBackImage/", null=True, blank=True,
                                               validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    clientPassportFrontImage = models.FileField(upload_to="clientPassportFrontImage/", null=True, blank=True,
                                               validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    clientPassportBackImage = models.FileField(upload_to="clientPassportBackImage/", null=True, blank=True,
                                               validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    clientForeignAddressProof = models.FileField(upload_to="clientForeignAddressProof/", null=True, blank=True,
                                               validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    clientForeignTaxIdentificationProof = models.FileField(upload_to="clientForeignTaxIdentificationProof/", null=True, blank=True,
                                               validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    clientCancelledChequeCopy = models.FileField(upload_to="clientCancelledChequeCopy/", null=True, blank=True,
                                               validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    clientBankAccountStatementOrPassbook = models.FileField(upload_to="clientBankAccountStatementOrPassbook/", null=True, blank=True,
                                               validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    clientChildrenBirthCertificate = models.FileField(upload_to="clientChildrenBirthCertificate/", null=True, blank=True,
                                               validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class ClientBankModel(models.Model):
    id = models.AutoField(primary_key=True)
    clientBankId = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name="clientBankId", null=True, blank=True)
    clientBankName = models.ForeignKey(BankNameModel, on_delete=models.CASCADE, related_name="clientBankName", null=True, blank=True)
    clientBankAccountType = models.CharField(max_length=500, null=True, blank=True)
    clientBankAccountNo = models.CharField(max_length=500, null=True, blank=True)
    clientBankIfsc = models.CharField(max_length=500, null=True, blank=True)
    clientBankMicr = models.CharField(max_length=500, null=True, blank=True)
    clientBankAddress = models.CharField(max_length=500, null=True, blank=True)
    clientBankBranch = models.CharField(max_length=500, null=True, blank=True)
    clientBankCity = models.CharField(max_length=500, null=True, blank=True)
    clientBankPincode = models.IntegerField(max_length=6, null=True, blank=True)
    clientPrimaryAccount = models.IntegerField(max_length=6, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class ClientTaxModel(models.Model):
    id = models.AutoField(primary_key=True)
    clientTaxId = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name="clientTaxId", null=True, blank=True)
    clientTaxIdDetail = models.CharField(max_length=500, null=True, blank=True)
    clientTaxIdNo = models.CharField(max_length=500, null=True, blank=True)
    clientTaxCountry = CountryField(blank_label='(select country)', null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class ClientPowerOfAttorneyModel(models.Model):
    id = models.AutoField(primary_key=True)
    clientPowerOfAttorneyId = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name="clientPowerOfAttorneyId", null=True, blank=True)
    clientPowerOfAttorneyName = models.CharField(max_length=500, null=True, blank=True)
    clientPowerOfAttorneyPanNo = models.CharField(max_length=500, null=True, blank=True)
    hideStatus = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


