from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import *
from .models import *


# Create your views here.


class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = UserTypeModel.objects.filter(hideStatus=0)
    serializer_class = UserTypeModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = UserTypeModelSerializers(UserTypeModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = UserTypeModelSerializers(UserTypeModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = UserTypeModelSerializers(data=request.data)
            else:
                serializer = UserTypeModelSerializers(instance=UserTypeModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        UserTypeModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class StateViewSet(viewsets.ModelViewSet):
    queryset = StateModel.objects.filter(hideStatus=0)
    serializer_class = StateModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = StateModelSerializers(StateModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = StateModelSerializers(StateModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = StateModelSerializers(data=request.data)
            else:
                serializer = StateModelSerializers(instance=StateModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        StateModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class CountryViewSet(viewsets.ModelViewSet):
    queryset = CountryModel.objects.filter(hideStatus=0)
    serializer_class = CountryModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = CountryModelSerializers(CountryModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = CountryModelSerializers(CountryModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = CountryModelSerializers(data=request.data)
            else:
                serializer = CountryModelSerializers(instance=CountryModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        CountryModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class GenderViewSet(viewsets.ModelViewSet):
    queryset = GenderModel.objects.filter(hideStatus=0)
    serializer_class = GenderModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = GenderModelSerializers(GenderModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = GenderModelSerializers(GenderModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = GenderModelSerializers(data=request.data)
            else:
                serializer = GenderModelSerializers(instance=GenderModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        GenderModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class MaritalStatusViewSet(viewsets.ModelViewSet):
    queryset = MaritalStatusModel.objects.filter(hideStatus=0)
    serializer_class = MaritalStatusModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = MaritalStatusModelSerializers(MaritalStatusModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = MaritalStatusModelSerializers(MaritalStatusModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = MaritalStatusModelSerializers(data=request.data)
            else:
                serializer = MaritalStatusModelSerializers(instance=MaritalStatusModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        MaritalStatusModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class PoliticallyExposedPersonViewSet(viewsets.ModelViewSet):
    queryset = PoliticallyExposedPersonModel.objects.filter(hideStatus=0)
    serializer_class = PoliticallyExposedPersonModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = PoliticallyExposedPersonModelSerializers(PoliticallyExposedPersonModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = PoliticallyExposedPersonModelSerializers(PoliticallyExposedPersonModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = PoliticallyExposedPersonModelSerializers(data=request.data)
            else:
                serializer = PoliticallyExposedPersonModelSerializers(instance=PoliticallyExposedPersonModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        PoliticallyExposedPersonModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class BankNameViewSet(viewsets.ModelViewSet):
    queryset = BankNameModel.objects.filter(hideStatus=0)
    serializer_class = BankNameModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = BankNameModelSerializers(BankNameModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = BankNameModelSerializers(BankNameModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = BankNameModelSerializers(data=request.data)
            else:
                serializer = BankNameModelSerializers(instance=BankNameModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        BankNameModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class GuardianRelationshipViewSet(viewsets.ModelViewSet):
    queryset = GuardianRelationshipModel.objects.filter(hideStatus=0)
    serializer_class = GuardianRelationshipModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = GuardianRelationshipModelSerializers(GuardianRelationshipModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = GuardianRelationshipModelSerializers(GuardianRelationshipModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = GuardianRelationshipModelSerializers(data=request.data)
            else:
                serializer = GuardianRelationshipModelSerializers(instance=GuardianRelationshipModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        GuardianRelationshipModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class ArnEntryViewSet(viewsets.ModelViewSet):
    queryset = ArnEntryModel.objects.filter(hideStatus=0)
    serializer_class = ArnEntryModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ArnEntryModelSerializers(ArnEntryModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = ArnEntryModelSerializers(ArnEntryModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ArnEntryModelSerializers(data=request.data)
            else:
                serializer = ArnEntryModelSerializers(instance=ArnEntryModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        ArnEntryModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class AmcEntryViewSet(viewsets.ModelViewSet):
    queryset = AmcEntryModel.objects.filter(hideStatus=0)
    serializer_class = AmcEntryModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = AmcEntryModelSerializers(AmcEntryModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = AmcEntryModelSerializers(AmcEntryModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = AmcEntryModelSerializers(data=request.data)
            else:
                serializer = AmcEntryModelSerializers(instance=AmcEntryModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        AmcEntryModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class AumEntryViewSet(viewsets.ModelViewSet):
    queryset = AumEntryModel.objects.filter(hideStatus=0)
    serializer_class = AumEntryModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = AumEntryModelSerializers(AumEntryModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = AumEntryModelSerializers(AumEntryModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = AumEntryModelSerializers(data=request.data)
            else:
                serializer = AumEntryModelSerializers(instance=AumEntryModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        AumEntryModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class CommissionEntryViewSet(viewsets.ModelViewSet):
    queryset = CommissionEntryModel.objects.filter(hideStatus=0)
    serializer_class = CommissionEntryModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = CommissionEntryModelSerializers(CommissionEntryModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = CommissionEntryModelSerializers(CommissionEntryModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = CommissionEntryModelSerializers(data=request.data)
            else:
                serializer = CommissionEntryModelSerializers(instance=CommissionEntryModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        CommissionEntryModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class AumYoyGrowthEntryViewSet(viewsets.ModelViewSet):
    queryset = AumYoyGrowthEntryModel.objects.filter(hideStatus=0)
    serializer_class = AumYoyGrowthEntryModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = AumYoyGrowthEntryModelSerializers(AumYoyGrowthEntryModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = AumYoyGrowthEntryModelSerializers(AumYoyGrowthEntryModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = AumYoyGrowthEntryModelSerializers(data=request.data)
            else:
                serializer = AumYoyGrowthEntryModelSerializers(instance=AumYoyGrowthEntryModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        AumYoyGrowthEntryModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class IndustryAumEntryViewSet(viewsets.ModelViewSet):
    queryset = IndustryAumEntryModel.objects.filter(hideStatus=0)
    serializer_class = IndustryAumEntryModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = IndustryAumEntryModelSerializers(IndustryAumEntryModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = IndustryAumEntryModelSerializers(IndustryAumEntryModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = IndustryAumEntryModelSerializers(data=request.data)
            else:
                serializer = IndustryAumEntryModelSerializers(instance=IndustryAumEntryModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        IndustryAumEntryModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class GstEntryViewSet(viewsets.ModelViewSet):
    queryset = GstEntryModel.objects.filter(hideStatus=0)
    serializer_class = GstEntryModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = GstEntryModelSerializers(GstEntryModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = GstEntryModelSerializers(GstEntryModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = GstEntryModelSerializers(data=request.data)
            else:
                serializer = GstEntryModelSerializers(instance=GstEntryModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        GstEntryModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class NavViewSet(viewsets.ModelViewSet):
    queryset = NavModel.objects.filter(hideStatus=0)
    serializer_class = NavModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = NavModelSerializers(NavModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = NavModelSerializers(NavModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = NavModelSerializers(data=request.data)
            else:
                serializer = NavModelSerializers(instance=NavModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        NavModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class IssueViewSet(viewsets.ModelViewSet):
    queryset = IssueModel.objects.filter(hideStatus=0)
    serializer_class = IssueModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = IssueModelSerializers(IssueModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = IssueModelSerializers(IssueModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = IssueModelSerializers(data=request.data)
            else:
                serializer = IssueModelSerializers(instance=IssueModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        IssueModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class StatementViewSet(viewsets.ModelViewSet):
    queryset = StatementModel.objects.filter(hideStatus=0)
    serializer_class = StatementModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = StatementModelSerializers(StatementModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = StatementModelSerializers(StatementModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = StatementModelSerializers(data=request.data)
            else:
                serializer = StatementModelSerializers(instance=StatementModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        StatementModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class CourierViewSet(viewsets.ModelViewSet):
    queryset = CourierModel.objects.filter(hideStatus=0)
    serializer_class = CourierModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = CourierModelSerializers(CourierModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = CourierModelSerializers(CourierModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = CourierModelSerializers(data=request.data)
            else:
                serializer = CourierModelSerializers(instance=CourierModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        CourierModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class FormsViewSet(viewsets.ModelViewSet):
    queryset = FormsModel.objects.filter(hideStatus=0)
    serializer_class = FormsModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = FormsModelSerializers(FormsModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = FormsModelSerializers(FormsModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = FormsModelSerializers(data=request.data)
            else:
                serializer = FormsModelSerializers(instance=FormsModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        FormsModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class MarketingViewSet(viewsets.ModelViewSet):
    queryset = MarketingModel.objects.filter(hideStatus=0)
    serializer_class = MarketingModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = MarketingModelSerializers(MarketingModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = MarketingModelSerializers(MarketingModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = MarketingModelSerializers(data=request.data)
            else:
                serializer = MarketingModelSerializers(instance=MarketingModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        MarketingModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = EmployeeModel.objects.filter(hideStatus=0)
    serializer_class = EmployeeModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = EmployeeModelSerializers(EmployeeModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = EmployeeModelSerializers(EmployeeModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = EmployeeModelSerializers(data=request.data)
            else:
                serializer = EmployeeModelSerializers(instance=EmployeeModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        EmployeeModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = ClientModel.objects.filter(hideStatus=0)
    serializer_class = ClientModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientModelSerializers(ClientModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = ClientModelSerializers(ClientModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientModelSerializers(data=request.data)
            else:
                serializer = ClientModelSerializers(instance=ClientModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        ClientModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class ClientFamilyDetailViewSet(viewsets.ModelViewSet):
    queryset = ClientFamilyDetailModel.objects.filter(hideStatus=0)
    serializer_class = ClientFamilyDetailModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientFamilyDetailModelSerializers(ClientFamilyDetailModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = ClientFamilyDetailModelSerializers(ClientFamilyDetailModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientFamilyDetailModelSerializers(data=request.data)
            else:
                serializer = ClientFamilyDetailModelSerializers(instance=ClientFamilyDetailModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        ClientFamilyDetailModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class ClientChildrenDetailViewSet(viewsets.ModelViewSet):
    queryset = ClientChildrenDetailModel.objects.filter(hideStatus=0)
    serializer_class = ClientChildrenDetailModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientChildrenDetailModelSerializers(ClientChildrenDetailModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = ClientChildrenDetailModelSerializers(ClientChildrenDetailModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientChildrenDetailModelSerializers(data=request.data)
            else:
                serializer = ClientChildrenDetailModelSerializers(instance=ClientChildrenDetailModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        ClientChildrenDetailModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class ClientPresentAddressViewSet(viewsets.ModelViewSet):
    queryset = ClientPresentAddressModel.objects.filter(hideStatus=0)
    serializer_class = ClientPresentAddressModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientPresentAddressModelSerializers(ClientPresentAddressModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = ClientPresentAddressModelSerializers(ClientPresentAddressModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientPresentAddressModelSerializers(data=request.data)
            else:
                serializer = ClientPresentAddressModelSerializers(instance=ClientPresentAddressModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        ClientPresentAddressModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class ClientPermanentAddressViewSet(viewsets.ModelViewSet):
    queryset = ClientPermanentAddressModel.objects.filter(hideStatus=0)
    serializer_class = ClientPermanentAddressModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientPermanentAddressModelSerializers(ClientPermanentAddressModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = ClientPermanentAddressModelSerializers(ClientPermanentAddressModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientPermanentAddressModelSerializers(data=request.data)
            else:
                serializer = ClientPermanentAddressModelSerializers(instance=ClientPermanentAddressModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        ClientPermanentAddressModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class ClientOfficeAddressViewSet(viewsets.ModelViewSet):
    queryset = ClientOfficeAddressModel.objects.filter(hideStatus=0)
    serializer_class = ClientOfficeAddressModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientOfficeAddressModelSerializers(ClientOfficeAddressModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = ClientOfficeAddressModelSerializers(ClientOfficeAddressModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientOfficeAddressModelSerializers(data=request.data)
            else:
                serializer = ClientOfficeAddressModelSerializers(instance=ClientOfficeAddressModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        ClientOfficeAddressModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class ClientOverseasAddressViewSet(viewsets.ModelViewSet):
    queryset = ClientOverseasAddressModel.objects.filter(hideStatus=0)
    serializer_class = ClientOverseasAddressModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientOverseasAddressModelSerializers(ClientOverseasAddressModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = ClientOverseasAddressModelSerializers(ClientOverseasAddressModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientOverseasAddressModelSerializers(data=request.data)
            else:
                serializer = ClientOverseasAddressModelSerializers(instance=ClientOverseasAddressModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        ClientOverseasAddressModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class ClientNomineeViewSet(viewsets.ModelViewSet):
    queryset = ClientNomineeModel.objects.filter(hideStatus=0)
    serializer_class = ClientNomineeModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientNomineeModelSerializers(ClientNomineeModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = ClientNomineeModelSerializers(ClientNomineeModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientNomineeModelSerializers(data=request.data)
            else:
                serializer = ClientNomineeModelSerializers(instance=ClientNomineeModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        ClientNomineeModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class ClientMedicalInsuranceViewSet(viewsets.ModelViewSet):
    queryset = ClientMedicalInsuranceModel.objects.filter(hideStatus=0)
    serializer_class = ClientMedicalInsuranceModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientMedicalInsuranceModelSerializers(ClientMedicalInsuranceModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = ClientMedicalInsuranceModelSerializers(ClientMedicalInsuranceModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientMedicalInsuranceModelSerializers(data=request.data)
            else:
                serializer = ClientMedicalInsuranceModelSerializers(instance=ClientMedicalInsuranceModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        ClientMedicalInsuranceModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class ClientTermInsuranceViewSet(viewsets.ModelViewSet):
    queryset = ClientTermInsuranceModel.objects.filter(hideStatus=0)
    serializer_class = ClientTermInsuranceModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientTermInsuranceModelSerializers(ClientTermInsuranceModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = ClientTermInsuranceModelSerializers(ClientTermInsuranceModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientTermInsuranceModelSerializers(data=request.data)
            else:
                serializer = ClientTermInsuranceModelSerializers(instance=ClientTermInsuranceModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        ClientTermInsuranceModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = TaskModel.objects.filter(hideStatus=0)
    serializer_class = TaskModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = TaskModelSerializers(TaskModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = TaskModelSerializers(TaskModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                      many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = TaskModelSerializers(data=request.data)
            else:
                serializer = TaskModelSerializers(instance=TaskModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        TaskModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)

