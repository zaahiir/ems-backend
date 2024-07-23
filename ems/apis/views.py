import base64
import logging
import traceback
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.http import JsonResponse
from django_countries import countries
from django_countries.fields import Country
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *

logger = logging.getLogger(__name__)


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Country):
            return str(obj)
        return super().default(obj)


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
        if request.headers.get('token'):
            if pk == "0":
                states = StateModel.objects.filter(hideStatus=0).order_by('-id')
            else:
                states = StateModel.objects.filter(hideStatus=0, id=pk).order_by('-id')
            serializer = StateModelSerializers(states, many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers.get('token'):
            if pk == "0":
                serializer = StateModelSerializers(data=request.data)
            else:
                instance = StateModel.objects.get(id=pk)
                serializer = StateModelSerializers(instance=instance, data=request.data)
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
        StateModel.objects.filter(id=pk).update(hideStatus=1)
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class ModeViewSet(viewsets.ModelViewSet):
    queryset = ModeModel.objects.filter(hideStatus=0)
    serializer_class = ModeModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers.get('token'):
            if pk == "0":
                modes = ModeModel.objects.filter(hideStatus=0).order_by('-id')
            else:
                modes = ModeModel.objects.filter(hideStatus=0, id=pk).order_by('-id')
            serializer = ModeModelSerializers(modes, many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers.get('token'):
            if pk == "0":
                serializer = ModeModelSerializers(data=request.data)
            else:
                instance = ModeModel.objects.get(id=pk)
                serializer = ModeModelSerializers(instance=instance, data=request.data)
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
        ModeModel.objects.filter(id=pk).update(hideStatus=1)
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class IssueTypeViewSet(viewsets.ModelViewSet):
    queryset = IssueTypeModel.objects.filter(hideStatus=0)
    serializer_class = IssueTypeModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = IssueTypeModelSerializers(IssueTypeModel.objects.filter(hideStatus=0).order_by('-id'),
                                                       many=True)
            else:
                serializer = IssueTypeModelSerializers(
                    IssueTypeModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                    many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = IssueTypeModelSerializers(data=request.data)
            else:
                serializer = IssueTypeModelSerializers(instance=IssueTypeModel.objects.get(id=pk), data=request.data)
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
        IssueTypeModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class FormTypeViewSet(viewsets.ModelViewSet):
    queryset = FormTypeModel.objects.filter(hideStatus=0)
    serializer_class = FormTypeModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = FormTypeModelSerializers(FormTypeModel.objects.filter(hideStatus=0).order_by('-id'),
                                                      many=True)
            else:
                serializer = FormTypeModelSerializers(
                    FormTypeModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                    many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = FormTypeModelSerializers(data=request.data)
            else:
                serializer = FormTypeModelSerializers(instance=FormTypeModel.objects.get(id=pk), data=request.data)
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
        FormTypeModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class GstTypeViewSet(viewsets.ModelViewSet):
    queryset = GstTypeModel.objects.filter(hideStatus=0)
    serializer_class = GstTypeModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = GstTypeModelSerializers(GstTypeModel.objects.filter(hideStatus=0).order_by('-id'),
                                                     many=True)
            else:
                serializer = GstTypeModelSerializers(
                    GstTypeModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                    many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = GstTypeModelSerializers(data=request.data)
            else:
                serializer = GstTypeModelSerializers(instance=GstTypeModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request", 'error': serializer.errors}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        GstTypeModel.objects.filter(id=pk).update(hideStatus='1')
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
                serializer = MaritalStatusModelSerializers(
                    MaritalStatusModel.objects.filter(hideStatus=0).order_by('-id'),
                    many=True)
            else:
                serializer = MaritalStatusModelSerializers(
                    MaritalStatusModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
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
                serializer = MaritalStatusModelSerializers(instance=MaritalStatusModel.objects.get(id=pk),
                                                           data=request.data)
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
                serializer = PoliticallyExposedPersonModelSerializers(
                    PoliticallyExposedPersonModel.objects.filter(hideStatus=0).order_by('-id'),
                    many=True)
            else:
                serializer = PoliticallyExposedPersonModelSerializers(
                    PoliticallyExposedPersonModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
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
                serializer = PoliticallyExposedPersonModelSerializers(
                    instance=PoliticallyExposedPersonModel.objects.get(id=pk), data=request.data)
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


class RelationshipViewSet(viewsets.ModelViewSet):
    queryset = RelationshipModel.objects.filter(hideStatus=0)
    serializer_class = RelationshipModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = RelationshipModelSerializers(
                    RelationshipModel.objects.filter(hideStatus=0).order_by('-id'),
                    many=True)
            else:
                serializer = RelationshipModelSerializers(
                    RelationshipModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                    many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = RelationshipModelSerializers(data=request.data)
            else:
                serializer = RelationshipModelSerializers(instance=RelationshipModel.objects.get(id=pk),
                                                                  data=request.data)
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
        RelationshipModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class AccountTypeViewSet(viewsets.ModelViewSet):
    queryset = AccountTypeModel.objects.filter(hideStatus=0)
    serializer_class = AccountTypeModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = AccountTypeModelSerializers(
                    AccountTypeModel.objects.filter(hideStatus=0).order_by('-id'),
                    many=True)
            else:
                serializer = AccountTypeModelSerializers(
                    AccountTypeModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                    many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = AccountTypeModelSerializers(data=request.data)
            else:
                serializer = AccountTypeModelSerializers(instance=AccountTypeModel.objects.get(id=pk),
                                                         data=request.data)
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
        AccountTypeModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class AccountPreferenceViewSet(viewsets.ModelViewSet):
    queryset = AccountPreferenceModel.objects.filter(hideStatus=0)
    serializer_class = AccountPreferenceModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = AccountPreferenceModelSerializers(
                    AccountPreferenceModel.objects.filter(hideStatus=0).order_by('-id'),
                    many=True)
            else:
                serializer = AccountPreferenceModelSerializers(
                    AccountPreferenceModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                    many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = AccountPreferenceModelSerializers(data=request.data)
            else:
                serializer = AccountPreferenceModelSerializers(instance=AccountPreferenceModel.objects.get(id=pk),
                                                               data=request.data)
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
        AccountPreferenceModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class ArnEntryViewSet(viewsets.ModelViewSet):
    queryset = ArnEntryModel.objects.filter(hideStatus=0)
    serializer_class = ArnEntryModelSerializers

    @action(detail=False, methods=['GET'])
    def countries(self, request):
        country_data = [{"code": code, "name": name} for code, name in list(countries)]
        return Response(country_data)

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

    @action(detail=False, methods=['GET'])
    def countries(self, request):
        country_data = [{"code": code, "name": name} for code, name in list(countries)]
        return Response(country_data)

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
                try:
                    instance = AmcEntryModel.objects.get(id=pk)
                except AmcEntryModel.DoesNotExist:
                    return Response({'code': 0, 'message': "AMC not found"}, status=404)
                serializer = AmcEntryModelSerializers(instance=instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                print("Serializer errors:", serializer.errors)
                response = {'code': 0, 'message': "Unable to Process Request", 'error': serializer.errors}
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
            data = request.data.copy()

            # Ensure aumMonth is in YYYY-MM format
            if 'aumMonth' in data:
                try:
                    # Validate the format
                    datetime.strptime(data['aumMonth'], '%Y-%m')
                except ValueError:
                    return Response({'code': 0, 'message': "Invalid aumMonth format. Use YYYY-MM."})
            if pk == "0":
                serializer = AumEntryModelSerializers(data=request.data)
            else:
                serializer = AumEntryModelSerializers(instance=AumEntryModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                print("Serializer errors:", serializer.errors)
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
                serializer = CommissionEntryModelSerializers(
                    CommissionEntryModel.objects.filter(hideStatus=0).order_by('-id'),
                    many=True)
            else:
                serializer = CommissionEntryModelSerializers(
                    CommissionEntryModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                    many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            data = request.data.copy()

            # Ensure aumMonth is in YYYY-MM format
            if 'aumMonth' in data:
                try:
                    # Validate the format
                    datetime.strptime(data['commissionMonth'], '%Y-%m')
                except ValueError:
                    return Response({'code': 0, 'message': "Invalid aumMonth format. Use YYYY-MM."})
            if pk == "0":
                serializer = CommissionEntryModelSerializers(data=request.data)
            else:
                serializer = CommissionEntryModelSerializers(instance=CommissionEntryModel.objects.get(id=pk),
                                                             data=request.data)
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
                serializer = AumYoyGrowthEntryModelSerializers(
                    AumYoyGrowthEntryModel.objects.filter(hideStatus=0).order_by('-id'),
                    many=True)
            else:
                serializer = AumYoyGrowthEntryModelSerializers(
                    AumYoyGrowthEntryModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
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
                serializer = AumYoyGrowthEntryModelSerializers(instance=AumYoyGrowthEntryModel.objects.get(id=pk),
                                                               data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                print(serializer.errors)
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
                serializer = IndustryAumEntryModelSerializers(
                    IndustryAumEntryModel.objects.filter(hideStatus=0).order_by('-id'),
                    many=True)
            else:
                serializer = IndustryAumEntryModelSerializers(
                    IndustryAumEntryModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
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
                serializer = IndustryAumEntryModelSerializers(instance=IndustryAumEntryModel.objects.get(id=pk),
                                                              data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                # print(serializer.errors)
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
            print("Serializer errors:", serializers.errors)
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
                serializer = StatementModelSerializers(
                    StatementModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
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
        if request.headers.get('token') != "":
            try:
                with transaction.atomic():
                    if pk == "0":
                        serializer = CourierModelSerializers(data=request.data)
                    else:
                        instance = CourierModel.objects.get(id=pk)
                        serializer = CourierModelSerializers(instance=instance, data=request.data, partial=True)

                    if serializer.is_valid():
                        serializer.save()
                        response = {'code': 1, 'message': "Done Successfully"}
                    else:
                        response = {'code': 0, 'message': "Unable to Process Request", 'errors': serializer.errors}
            except ValidationError as e:
                response = {'code': 0, 'message': "File validation error", 'errors': str(e)}
            except Exception as e:
                response = {'code': 0, 'message': str(e)}
        else:
            response = {'code': 0, 'message': "Token is invalid"}

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        CourierModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class CourierFileViewSet(viewsets.ModelViewSet):
    queryset = CourierFileModel.objects.filter(hideStatus=0)
    serializer_class = CourierFileModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers.get('token') != "":
            files = CourierFileModel.objects.filter(courier_id=pk, hideStatus=0)
            serializer = CourierFileModelSerializers(files, many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All Files Retrieved"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        try:
            file = CourierFileModel.objects.get(id=pk)
            file.hideStatus = '1'
            file.save()
            response = {'code': 1, 'message': "File Deleted Successfully"}
        except CourierFileModel.DoesNotExist:
            response = {'code': 0, 'message': "File not found"}
        except Exception as e:
            response = {'code': 0, 'message': str(e)}
        return Response(response)


from rest_framework import status

from rest_framework import status


class FormsViewSet(viewsets.ModelViewSet):
    queryset = FormsModel.objects.filter(hideStatus=0)
    serializer_class = FormsModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers.get('token') != "":
            if pk == "0":
                serializer = FormsModelSerializers(FormsModel.objects.filter(hideStatus=0).order_by('-id'), many=True)
            else:
                serializer = FormsModelSerializers(FormsModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                   many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All Retrieved"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers.get('token') != "":
            if pk == "0":
                serializer = FormsModelSerializers(data=request.data)
            else:
                instance = FormsModel.objects.get(id=pk)
                serializer = FormsModelSerializers(instance=instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request", "error": serializer.errors}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response, status=status.HTTP_200_OK)

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
                serializer = MarketingModelSerializers(
                    MarketingModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                    many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers.get('token') != "":
            if pk == "0":
                serializer = MarketingModelSerializers(data=request.data)
            else:
                instance = MarketingModel.objects.get(id=pk)
                serializer = MarketingModelSerializers(instance=instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request", 'errors': serializer.errors}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        MarketingModel.objects.filter(id=pk).update(hideStatus='1')
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
            print("Received data:", request.data)  # Debug print
            if pk == "0":
                serializer = TaskModelSerializers(data=request.data)
            else:
                serializer = TaskModelSerializers(instance=TaskModel.objects.get(id=pk), data=request.data)
            if serializer.is_valid():
                print("Validated data:", serializer.validated_data)  # Debug print
                serializer.save()
                print("Saved task:", serializer.__dict__)  # Debug print
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                print("Serializer errors:", serializer.errors)  # Debug print
                response = {'code': 0, 'message': "Unable to Process Request"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        TaskModel.objects.filter(id=pk).update(hideStatus='1')
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
                print("one")
            if serializer.is_valid():
                print("two")
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                print("Serializer errors:", serializer.errors)
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

    @action(detail=False, methods=['GET'])
    def countries(self, request):
        country_data = [{"code": code, "name": name} for code, name in list(countries)]
        return Response(country_data)

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers.get('token'):
            if pk == "0":
                serializer = ClientModelSerializers(ClientModel.objects.filter(hideStatus=0).order_by('-id'), many=True)
            else:
                serializer = ClientModelSerializers(ClientModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                    many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All Retrieved"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return JsonResponse(response, encoder=CustomJSONEncoder)

    @action(detail=True, methods=['GET'])
    def listing_client(self, request, pk=None):
        if request.headers.get('token'):
            try:
                client = ClientModelSerializers(ClientModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                many=True)
                client_family = ClientFamilyDetailModelSerializers(
                    ClientFamilyDetailModel.objects.filter(hideStatus=0, clientFamilyDetailId=pk).order_by('-id'),
                    many=True)
                client_children = ClientChildrenDetailModelSerializers(
                    ClientChildrenDetailModel.objects.filter(hideStatus=0, clientChildrenId=pk).order_by('-id'),
                    many=True)
                client_present_address = ClientPresentAddressModelSerializers(
                    ClientPresentAddressModel.objects.filter(hideStatus=0, clientPresentAddressId=pk).order_by('-id'),
                    many=True)
                client_permanent_address = ClientPermanentAddressModelSerializers(
                    ClientPermanentAddressModel.objects.filter(hideStatus=0, clientPermanentAddressId=pk).order_by(
                        '-id'), many=True)
                client_office_address = ClientOfficeAddressModelSerializers(
                    ClientOfficeAddressModel.objects.filter(hideStatus=0, clientOfficeAddressId=pk).order_by('-id'),
                    many=True)
                client_overseas_address = ClientOverseasAddressModelSerializers(
                    ClientOverseasAddressModel.objects.filter(hideStatus=0, clientOverseasAddressId=pk).order_by('-id'),
                    many=True)
                client_nominee = ClientNomineeModelSerializers(
                    ClientNomineeModel.objects.filter(hideStatus=0, clientNomineeId=pk).order_by('-id'), many=True)
                client_insurance = ClientInsuranceModelSerializers(
                    ClientInsuranceModel.objects.filter(hideStatus=0, clientInsuranceId=pk).order_by('-id'), many=True)
                client_medical_insurance = ClientMedicalInsuranceModelSerializers(
                    ClientMedicalInsuranceModel.objects.filter(hideStatus=0, clientMedicalInsuranceId=pk).order_by(
                        '-id'), many=True)
                client_term_insurance = ClientTermInsuranceModelSerializers(
                    ClientTermInsuranceModel.objects.filter(hideStatus=0, clientTermInsuranceId=pk).order_by('-id'),
                    many=True)
                client_upload_files = ClientUploadFileModelSerializers(
                    ClientUploadFileModel.objects.filter(hideStatus=0, clientUploadFileId=pk).order_by('-id'),
                    many=True)
                client_bank = ClientBankModelSerializers(
                    ClientBankModel.objects.filter(hideStatus=0, clientBankId=pk).order_by('-id'), many=True)
                client_tax = ClientTaxModelSerializers(
                    ClientTaxModel.objects.filter(hideStatus=0, clientTaxId=pk).order_by('-id'), many=True)
                client_attorney = ClientPowerOfAttorneyModelSerializers(
                    ClientPowerOfAttorneyModel.objects.filter(hideStatus=0, clientPowerOfAttorneyId=pk).order_by('-id'),
                    many=True)
                client_guardian = ClientGuardianModelSerializers(
                    ClientGuardianModel.objects.filter(hideStatus=0, clientGuardianId=pk).order_by('-id'),
                    many=True)

                combined_serializer = {
                    "client": client.data,
                    "family": client_family.data,
                    "children": client_children.data,
                    "present_address": client_present_address.data,
                    "permanent_address": client_permanent_address.data,
                    "office_address": client_office_address.data,
                    "overseas_address": client_overseas_address.data,
                    "nominee": client_nominee.data,
                    "insurance": client_insurance.data,
                    "medical_insurance": client_medical_insurance.data,
                    "term_insurance": client_term_insurance.data,
                    "upload_files": client_upload_files.data,
                    "bank": client_bank.data,
                    "tax": client_tax.data,
                    "attorney": client_attorney.data,
                    "guardian": client_guardian.data,
                }
                return JsonResponse({'code': 1, 'data': combined_serializer, 'message': "All Retrieved"},
                                    encoder=CustomJSONEncoder)
            except Exception as e:
                error_message = str(e)
                stack_trace = traceback.format_exc()
                return Response({
                    'code': 0,
                    'message': "An error occurred while retrieving client data",
                    'error': error_message,
                    'stack_trace': stack_trace
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'code': 0, 'data': [], 'message': "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['POST'])
    @transaction.atomic
    def processing(self, request, pk=None):
        if request.headers.get('token'):
            try:
                with transaction.atomic():
                    # Process main client data
                    client_data = request.data.get('clientJson', {})
                    if pk == "0":
                        client_serializer = ClientModelSerializers(data=client_data)
                    else:
                        client_instance = ClientModel.objects.get(id=pk)
                        client_serializer = ClientModelSerializers(instance=client_instance, data=client_data)
                    if client_serializer.is_valid():
                        client_instance = client_serializer.save()
                        client_id = client_instance.id
                    else:
                        print(client_serializer.errors)
                        return Response(
                            {'code': 0, 'message': "Invalid client data", 'errors': client_serializer.errors})

                    # Process family details
                    family_data = request.data.get('familyJson', {})
                    family_instance, created = ClientFamilyDetailModel.objects.get_or_create(
                        clientFamilyDetailId=client_instance)
                    family_serializer = ClientFamilyDetailModelSerializers(instance=family_instance, data=family_data)
                    if family_serializer.is_valid():
                        family_serializer.save()
                    else:
                        return Response(
                            {'code': 0, 'message': "Invalid family data", 'errors': family_serializer.errors})

                    # Process children
                    children_data = request.data.get('childrenJson', [])
                    existing_children = ClientChildrenDetailModel.objects.filter(clientChildrenId=client_instance)
                    existing_children_ids = set(existing_children.values_list('id', flat=True))

                    processed_children_ids = set()

                    for child_data in children_data:
                        child_id = child_data.get('id')
                        if child_id:
                            child_instance = existing_children.filter(id=child_id).first()
                            if child_instance:
                                child_serializer = ClientChildrenDetailModelSerializers(instance=child_instance,
                                                                                        data=child_data)
                                processed_children_ids.add(child_id)
                            else:
                                child_serializer = ClientChildrenDetailModelSerializers(data=child_data)
                        else:
                            child_serializer = ClientChildrenDetailModelSerializers(data=child_data)

                        if child_serializer.is_valid():
                            child_serializer.save(clientChildrenId=client_instance)
                        else:
                            return Response(
                                {'code': 0, 'message': "Invalid child data", 'errors': child_serializer.errors})

                    # Delete children that were not in the submitted data
                    children_to_delete = existing_children_ids - processed_children_ids
                    ClientChildrenDetailModel.objects.filter(id__in=children_to_delete).delete()

                    # Process addresses
                    addresses_types = [
                        ('presentAddressJson', ClientPresentAddressModelSerializers, 'clientPresentAddressId'),
                        ('permanentAddressJson', ClientPermanentAddressModelSerializers, 'clientPermanentAddressId'),
                        ('officeAddressJson', ClientOfficeAddressModelSerializers, 'clientOfficeAddressId'),
                        ('overseasAddressJson', ClientOverseasAddressModelSerializers, 'clientOverseasAddressId'),
                    ]
                    for address_key, serializer_class, client_field in addresses_types:
                        address_data = request.data.get(address_key, {})
                        logger.debug(f"Processing {address_key}: {address_data}")
                        if address_data:
                            address_instance, created = serializer_class.Meta.model.objects.get_or_create(
                                **{client_field: client_instance})
                            address_serializer = serializer_class(instance=address_instance, data=address_data)
                            if address_serializer.is_valid():
                                address_serializer.save(**{client_field: client_instance})
                            else:
                                logger.error(f"Invalid {address_key} data: {address_serializer.errors}")
                                return Response({'code': 0, 'message': f"Invalid {address_key} data",
                                                 'errors': address_serializer.errors})

                    # Process nominees
                    nominee_data = request.data.get('nomineeJson', [])
                    ClientNomineeModel.objects.filter(clientNomineeId=client_instance).delete()
                    for nominee in nominee_data:
                        nominee_serializer = ClientNomineeModelSerializers(data=nominee)
                        if nominee_serializer.is_valid():
                            nominee_serializer.save(clientNomineeId=client_instance)
                        else:
                            return Response(
                                {'code': 0, 'message': "Invalid nominee data", 'errors': nominee_serializer.errors})

                    # Process insurance policies
                    insurance_types = [
                        ('insuranceJson', ClientInsuranceModelSerializers, 'clientInsuranceId'),
                        ('medicalInsuranceJson', ClientMedicalInsuranceModelSerializers, 'clientMedicalInsuranceId'),
                        ('termInsuranceJson', ClientTermInsuranceModelSerializers, 'clientTermInsuranceId'),
                    ]
                    for insurance_key, serializer_class, client_field in insurance_types:
                        insurance_data = request.data.get(insurance_key, [])

                        # Delete existing records
                        serializer_class.Meta.model.objects.filter(**{client_field: client_instance}).delete()

                        # Create new records
                        for policy in insurance_data:
                            policy[client_field] = client_instance.id
                            policy_serializer = serializer_class(data=policy)
                            if policy_serializer.is_valid():
                                policy_serializer.save()
                            else:
                                return Response({'code': 0, 'message': f"Invalid {insurance_key} data",
                                                 'errors': policy_serializer.errors})

                    # Process file uploads
                    upload_files_data = request.data.get('uploadFilesJson', {})
                    # Always create or get the file instance
                    file_instance, created = ClientUploadFileModel.objects.get_or_create(
                        clientUploadFileId=client_instance)
                    if upload_files_data:
                        for field_name, file_data in upload_files_data.items():
                            if file_data:
                                if isinstance(file_data, str) and file_data.startswith('data:'):
                                    # Handle base64 encoded data
                                    format, imgstr = file_data.split(';base64,')
                                    ext = format.split('/')[-1]
                                    data = ContentFile(base64.b64decode(imgstr), name=f'{field_name}.{ext}')
                                elif isinstance(file_data, dict) and 'name' in file_data and 'content' in file_data:
                                    # Handle dictionary with name and content
                                    ext = file_data['name'].split('.')[-1]
                                    data = ContentFile(base64.b64decode(file_data['content']), name=file_data['name'])
                                else:
                                    # Unsupported format
                                    logger.warning(f"Unexpected file data format for {field_name}: {type(file_data)}")
                                    continue

                            setattr(file_instance, field_name, data)

                    # Save the instance even if no files were uploaded
                    file_instance.save()

                    # Process bank details
                    bank_data = request.data.get('bankJson', [])
                    ClientBankModel.objects.filter(clientBankId=client_instance).delete()
                    for bank in bank_data:
                        bank_serializer = ClientBankModelSerializers(data=bank)
                        if bank_serializer.is_valid():
                            bank_serializer.save(clientBankId=client_instance)
                        else:
                            return Response(
                                {'code': 0, 'message': "Invalid bank data", 'errors': bank_serializer.errors})

                    # Process tax details
                    tax_data = request.data.get('taxJson', {})
                    tax_instance, created = ClientTaxModel.objects.get_or_create(clientTaxId=client_instance)
                    tax_serializer = ClientTaxModelSerializers(instance=tax_instance, data=tax_data)
                    if tax_serializer.is_valid():
                        tax_serializer.save(clientTaxId=client_instance)
                    else:
                        return Response({'code': 0, 'message': "Invalid tax data", 'errors': tax_serializer.errors})

                    # Process guardian details
                    guardian_data = request.data.get('guardianJSON', {})
                    guardian_instance, created = ClientGuardianModel.objects.get_or_create(clientGuardianId=client_instance)
                    guardian_serializer = ClientTaxModelSerializers(instance=guardian_instance, data=guardian_data)
                    if guardian_serializer.is_valid():
                        guardian_serializer.save(clientGuardianId=client_instance)
                    else:
                        return Response({'code': 0, 'message': "Invalid tax data", 'errors': guardian_serializer.errors})

                    # Process power of attorney
                    attorney_data = request.data.get('attorneyJson', {})
                    attorney_instance, created = ClientPowerOfAttorneyModel.objects.get_or_create(
                        clientPowerOfAttorneyId=client_instance)

                    # Handle file upload for attorney
                    attorney_upload = attorney_data.get('clientPowerOfAttorneyUpload')
                    if attorney_upload:
                        if isinstance(attorney_upload, str) and attorney_upload.startswith('data:'):
                            # Handle base64 encoded data
                            format, imgstr = attorney_upload.split(';base64,')
                            ext = format.split('/')[-1]
                            data = ContentFile(base64.b64decode(imgstr), name=f'attorney_upload.{ext}')
                            attorney_instance.clientPowerOfAttorneyUpload = data
                        else:
                            # Handle as regular file upload
                            attorney_instance.clientPowerOfAttorneyUpload = attorney_upload

                    # Remove the file from the data before serialization
                    if 'clientPowerOfAttorneyUpload' in attorney_data:
                        del attorney_data['clientPowerOfAttorneyUpload']

                    attorney_serializer = ClientPowerOfAttorneyModelSerializers(instance=attorney_instance,
                                                                                data=attorney_data)
                    if attorney_serializer.is_valid():
                        attorney_serializer.save(clientPowerOfAttorneyId=client_instance)
                    else:
                        print(attorney_serializer.errors)
                        return Response(
                            {'code': 0, 'message': "Invalid attorney data", 'errors': attorney_serializer.errors})

                    return Response({'code': 1, 'message': "Client data processed successfully"})
            except Exception as e:
                return Response({'code': 0, 'message': f"An error occurred: {str(e)}"})
        else:
            return Response({'code': 0, 'message': "Token is invalid"})

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        try:
            with transaction.atomic():
                client = ClientModel.objects.get(id=pk)

                # Update hideStatus for the main client
                client.hideStatus = '1'
                client.save()

                # Update hideStatus for related models
                # Note: You'll need to add the hideStatus field to these models if it doesn't exist
                ClientFamilyDetailModel.objects.filter(clientFamilyDetailId=client).update(hideStatus='1')
                ClientChildrenDetailModel.objects.filter(clientChildrenId=client).update(hideStatus='1')
                ClientPresentAddressModel.objects.filter(clientPresentAddressId=client).update(hideStatus='1')
                ClientPermanentAddressModel.objects.filter(clientPermanentAddressId=client).update(hideStatus='1')
                ClientOfficeAddressModel.objects.filter(clientOfficeAddressId=client).update(hideStatus='1')
                ClientOverseasAddressModel.objects.filter(clientOverseasAddressId=client).update(hideStatus='1')
                ClientNomineeModel.objects.filter(clientNomineeId=client).update(hideStatus='1')
                ClientInsuranceModel.objects.filter(clientInsuranceId=client).update(hideStatus='1')
                ClientMedicalInsuranceModel.objects.filter(clientMedicalInsuranceId=client).update(hideStatus='1')
                ClientTermInsuranceModel.objects.filter(clientTermInsuranceId=client).update(hideStatus='1')
                ClientUploadFileModel.objects.filter(clientUploadFileId=client).update(hideStatus='1')
                ClientBankModel.objects.filter(clientBankId=client).update(hideStatus='1')
                ClientTaxModel.objects.filter(clientTaxId=client).update(hideStatus='1')
                ClientPowerOfAttorneyModel.objects.filter(clientPowerOfAttorneyId=client).update(hideStatus='1')
                ClientGuardianModel.objects.filter(clientGuardianId=client).update(hideStatus='1')

            return Response({'code': 1, 'message': "Client and all related data hidden successfully"})
        except ClientModel.DoesNotExist:
            return Response({'code': 0, 'message': "Client not found"}, status=404)
        except Exception as e:
            return Response({'code': 0, 'message': f"An error occurred: {str(e)}"}, status=500)


class ClientFamilyDetailViewSet(viewsets.ModelViewSet):
    queryset = ClientFamilyDetailModel.objects.filter(hideStatus=0)
    serializer_class = ClientFamilyDetailModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientFamilyDetailModelSerializers(
                    ClientFamilyDetailModel.objects.filter(hideStatus=0).order_by('-id'),
                    many=True)
            else:
                serializer = ClientFamilyDetailModelSerializers(
                    ClientFamilyDetailModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
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
                serializer = ClientFamilyDetailModelSerializers(instance=ClientFamilyDetailModel.objects.get(id=pk),
                                                                data=request.data)
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
                serializer = ClientChildrenDetailModelSerializers(
                    ClientChildrenDetailModel.objects.filter(hideStatus=0).order_by('-id'),
                    many=True)
            else:
                serializer = ClientChildrenDetailModelSerializers(
                    ClientChildrenDetailModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
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
                serializer = ClientChildrenDetailModelSerializers(instance=ClientChildrenDetailModel.objects.get(id=pk),
                                                                  data=request.data)
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
                serializer = ClientPresentAddressModelSerializers(
                    ClientPresentAddressModel.objects.filter(hideStatus=0).order_by('-id'),
                    many=True)
            else:
                serializer = ClientPresentAddressModelSerializers(
                    ClientPresentAddressModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
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
                serializer = ClientPresentAddressModelSerializers(instance=ClientPresentAddressModel.objects.get(id=pk),
                                                                  data=request.data)
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
                serializer = ClientPermanentAddressModelSerializers(
                    ClientPermanentAddressModel.objects.filter(hideStatus=0).order_by('-id'),
                    many=True)
            else:
                serializer = ClientPermanentAddressModelSerializers(
                    ClientPermanentAddressModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
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
                serializer = ClientPermanentAddressModelSerializers(
                    instance=ClientPermanentAddressModel.objects.get(id=pk), data=request.data)
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
                serializer = ClientOfficeAddressModelSerializers(
                    ClientOfficeAddressModel.objects.filter(hideStatus=0).order_by('-id'),
                    many=True)
            else:
                serializer = ClientOfficeAddressModelSerializers(
                    ClientOfficeAddressModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
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
                serializer = ClientOfficeAddressModelSerializers(instance=ClientOfficeAddressModel.objects.get(id=pk),
                                                                 data=request.data)
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
                serializer = ClientOverseasAddressModelSerializers(
                    ClientOverseasAddressModel.objects.filter(hideStatus=0).order_by('-id'),
                    many=True)
            else:
                serializer = ClientOverseasAddressModelSerializers(
                    ClientOverseasAddressModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
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
                serializer = ClientOverseasAddressModelSerializers(
                    instance=ClientOverseasAddressModel.objects.get(id=pk), data=request.data)
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
                serializer = ClientNomineeModelSerializers(
                    ClientNomineeModel.objects.filter(hideStatus=0).order_by('-id'),
                    many=True)
            else:
                serializer = ClientNomineeModelSerializers(
                    ClientNomineeModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
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
                serializer = ClientNomineeModelSerializers(instance=ClientNomineeModel.objects.get(id=pk),
                                                           data=request.data)
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
                serializer = ClientMedicalInsuranceModelSerializers(
                    ClientMedicalInsuranceModel.objects.filter(hideStatus=0).order_by('-id'),
                    many=True)
            else:
                serializer = ClientMedicalInsuranceModelSerializers(
                    ClientMedicalInsuranceModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
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
                serializer = ClientMedicalInsuranceModelSerializers(
                    instance=ClientMedicalInsuranceModel.objects.get(id=pk), data=request.data)
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
                serializer = ClientTermInsuranceModelSerializers(
                    ClientTermInsuranceModel.objects.filter(hideStatus=0).order_by('-id'),
                    many=True)
            else:
                serializer = ClientTermInsuranceModelSerializers(
                    ClientTermInsuranceModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
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
                serializer = ClientTermInsuranceModelSerializers(instance=ClientTermInsuranceModel.objects.get(id=pk),
                                                                 data=request.data)
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


class ClientUploadFileViewSet(viewsets.ModelViewSet):
    queryset = ClientUploadFileModel.objects.filter(hideStatus=0)
    serializer_class = ClientUploadFileModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientUploadFileModelSerializers(
                    ClientUploadFileModel.objects.filter(hideStatus=0).order_by('-id'),
                    many=True)
            else:
                serializer = ClientUploadFileModelSerializers(
                    ClientUploadFileModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                    many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientUploadFileModelSerializers(data=request.data)
            else:
                serializer = ClientUploadFileModelSerializers(instance=ClientUploadFileModel.objects.get(id=pk),
                                                              data=request.data)
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
        ClientUploadFileModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class ClientBankViewSet(viewsets.ModelViewSet):
    queryset = ClientBankModel.objects.filter(hideStatus=0)
    serializer_class = ClientBankModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientBankModelSerializers(ClientBankModel.objects.filter(hideStatus=0).order_by('-id'),
                                                        many=True)
            else:
                serializer = ClientBankModelSerializers(
                    ClientBankModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                    many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientBankModelSerializers(data=request.data)
            else:
                serializer = ClientBankModelSerializers(instance=ClientBankModel.objects.get(id=pk), data=request.data)
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
        ClientBankModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class ClientTaxViewSet(viewsets.ModelViewSet):
    queryset = ClientTaxModel.objects.filter(hideStatus=0)
    serializer_class = ClientTaxModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientTaxModelSerializers(ClientTaxModel.objects.filter(hideStatus=0).order_by('-id'),
                                                       many=True)
            else:
                serializer = ClientTaxModelSerializers(
                    ClientTaxModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                    many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientTaxModelSerializers(data=request.data)
            else:
                serializer = ClientTaxModelSerializers(instance=ClientTaxModel.objects.get(id=pk), data=request.data)
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
        ClientTaxModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)


class ClientPowerOfAttorneyViewSet(viewsets.ModelViewSet):
    queryset = ClientPowerOfAttorneyModel.objects.filter(hideStatus=0)
    serializer_class = ClientPowerOfAttorneyModelSerializers

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientPowerOfAttorneyModelSerializers(
                    ClientPowerOfAttorneyModel.objects.filter(hideStatus=0).order_by('-id'),
                    many=True)
            else:
                serializer = ClientPowerOfAttorneyModelSerializers(
                    ClientPowerOfAttorneyModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                    many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        if request.headers['token'] != "":
            if pk == "0":
                serializer = ClientPowerOfAttorneyModelSerializers(data=request.data)
            else:
                serializer = ClientPowerOfAttorneyModelSerializers(
                    instance=ClientPowerOfAttorneyModel.objects.get(id=pk), data=request.data)
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
        ClientPowerOfAttorneyModel.objects.filter(id=pk).update(hideStatus='1')
        response = {'code': 1, 'message': "Done Successfully"}
        return Response(response)
