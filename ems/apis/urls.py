from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import *

router = routers.DefaultRouter()

router.register('userType', UserTypeViewSet),
router.register('state', StateViewSet),
router.register('country', CountryViewSet),
# router.register('gender', GenderViewSet),
# router.register('politicallyExposedPerson', PoliticallyExposedPersonViewSet),
# router.register('bankName', BankNameViewSet),
# router.register('guardianRelationship', GuardianRelationshipViewSet),
# router.register('defaultAccount', DefaultAccountViewSet),
router.register('arnEntry', ArnEntryViewSet),
router.register('amcEntry', AmcEntryViewSet),
router.register('aumEntry', AumEntryViewSet),
router.register('commissionEntry', CommissionEntryViewSet),
router.register('aumYoyGrowthEntry', AumYoyGrowthEntryViewSet),
router.register('industryAumEntry', IndustryAumEntryViewSet),
router.register('gstEntry', GstEntryViewSet),
router.register('nav', NavViewSet),
router.register('issue', IssueViewSet),
router.register('statement', StatementViewSet),
router.register('courier', CourierViewSet),
router.register('forms', FormsViewSet),
router.register('marketing', MarketingViewSet),
# router.register('employee', EmployeeViewSet),
# router.register('client', ClientViewSet),
# router.register('clientFamilyDetail', ClientFamilyDetailViewSet),
# router.register('clientChildrenDetail', ClientChildrenDetailViewSet),
# router.register('clientPresentAddress', ClientPresentAddressViewSet),
# router.register('clientPermanentAddress', ClientPermanentAddressViewSet),
# router.register('clientOfficeAddress', ClientOfficeAddressViewSet),
# router.register('clientOverseasAddress', ClientOverseasAddressViewSet),
# router.register('clientNominee', ClientNomineeViewSet),
# router.register('clientMedicalInsurance', ClientMedicalInsuranceViewSet),
# router.register('clientTermInsurance', ClientTermInsuranceViewSet),
# router.register('clientUploadFile', ClientUploadFileViewSet),
# router.register('clientBank', ClientBankViewSet),
# router.register('clientTax', ClientTaxViewSet),
# router.register('task', TaskViewSet),


urlpatterns = [
    path('', include(router.urls)),
]