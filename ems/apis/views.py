import base64
import traceback
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django_countries import countries
from django_countries.fields import Country
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import connection
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
import urllib.parse
from .serializers import *
from django.http import JsonResponse
from datetime import datetime, timedelta
from .utils import get_tokens_for_user
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import CursorPagination
from django.core.management import call_command
from django.db.models import Q
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Max

logger = logging.getLogger(__name__)


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Country):
            return str(obj)
        return super().default(obj)


class UserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        dob = request.data.get('dob')

        if not username:
            return Response({"detail": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate superuser
        user = authenticate(username=username, password=password)
        if user and user.is_superuser:
            tokens = get_tokens_for_user({
                'username': user.username,
                'id': user.id,
                'user_type': 'superuser'
            })
            return Response({
                **tokens,
                'user_type': 'superuser',
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
            }, status=status.HTTP_200_OK)

        # Check Employee credentials
        employee = EmployeeModel.objects.filter(employeeEmail=username).first()
        if employee:
            if not password:
                return Response({"detail": "Password is required for employee login"},
                                status=status.HTTP_400_BAD_REQUEST)

            if employee.check_password(password):
                tokens = get_tokens_for_user({
                    'username': employee.employeeEmail,
                    'id': employee.id,
                    'user_type': 'employee'
                })
                return Response({
                    **tokens,
                    'user_type': 'employee',
                    'user_id': employee.id,
                    'name': employee.employeeName,
                    'email': employee.employeeEmail,
                    'user_type_id': employee.employeeUserType.id if employee.employeeUserType else None,
                    'user_type_name': employee.employeeUserType.userTypeName if employee.employeeUserType else None,
                }, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid password for employee"}, status=status.HTTP_401_UNAUTHORIZED)

        # Check Client credentials
        if not dob:
            return Response({"detail": "Date of Birth is required for client login"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
        except ValueError:
            return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        client = ClientModel.objects.filter(clientPanNo=username, clientDateOfBirth=dob_date).first()
        if client:
            tokens = get_tokens_for_user({
                'username': client.clientPanNo,
                'id': client.id,
                'user_type': 'client'
            })
            return Response({
                **tokens,
                'user_type': 'client',
                'user_id': client.id,
                'name': client.clientName,
                'email': client.clientEmail,
            }, status=status.HTTP_200_OK)

        return Response({"detail": "No user found with provided credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if user.is_superuser:
            return Response({
                'user_type': 'superuser',
                'user_id': user.id,
                'username': user.username,
                'name': user.username,  # Use username as name for superusers
                'email': user.email,
            }, status=status.HTTP_200_OK)

        try:
            employee = EmployeeModel.objects.get(employeeEmail=user.email)
            serializer = EmployeeModelSerializers(employee, context={'request': request})
            return Response({
                'user_type': 'employee',
                **serializer.data
            }, status=status.HTTP_200_OK)
        except EmployeeModel.DoesNotExist:
            pass

        try:
            client = ClientModel.objects.get(clientEmail=user.email)
            return Response({
                'user_type': 'client',
                'user_id': client.id,
                'name': client.clientName,
                'email': client.clientEmail,
                'pan_no': client.clientPanNo,
                'date_of_birth': client.clientDateOfBirth,
            }, status=status.HTTP_200_OK)
        except ClientModel.DoesNotExist:
            pass

        return Response({'detail': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                raise ValidationError("Refresh token is required")

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": "An error occurred during logout"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = UserTypeModel.objects.filter(hideStatus=0)
    serializer_class = UserTypeModelSerializers
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access these views

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            UserTypeModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class StateViewSet(viewsets.ModelViewSet):
    queryset = StateModel.objects.filter(hideStatus=0)
    serializer_class = StateModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            StateModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class ModeViewSet(viewsets.ModelViewSet):
    queryset = ModeModel.objects.filter(hideStatus=0)
    serializer_class = ModeModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            ModeModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class IssueTypeViewSet(viewsets.ModelViewSet):
    queryset = IssueTypeModel.objects.filter(hideStatus=0)
    serializer_class = IssueTypeModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            IssueTypeModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class FormTypeViewSet(viewsets.ModelViewSet):
    queryset = FormTypeModel.objects.filter(hideStatus=0)
    serializer_class = FormTypeModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            FormTypeModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class GstTypeViewSet(viewsets.ModelViewSet):
    queryset = GstTypeModel.objects.filter(hideStatus=0)
    serializer_class = GstTypeModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            GstTypeModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class GenderViewSet(viewsets.ModelViewSet):
    queryset = GenderModel.objects.filter(hideStatus=0)
    serializer_class = GenderModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            GenderModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class MaritalStatusViewSet(viewsets.ModelViewSet):
    queryset = MaritalStatusModel.objects.filter(hideStatus=0)
    serializer_class = MaritalStatusModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            MaritalStatusModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class PoliticallyExposedPersonViewSet(viewsets.ModelViewSet):
    queryset = PoliticallyExposedPersonModel.objects.filter(hideStatus=0)
    serializer_class = PoliticallyExposedPersonModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            PoliticallyExposedPersonModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class BankNameViewSet(viewsets.ModelViewSet):
    queryset = BankNameModel.objects.filter(hideStatus=0)
    serializer_class = BankNameModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            BankNameModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class RelationshipViewSet(viewsets.ModelViewSet):
    queryset = RelationshipModel.objects.filter(hideStatus=0)
    serializer_class = RelationshipModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            RelationshipModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class AccountTypeViewSet(viewsets.ModelViewSet):
    queryset = AccountTypeModel.objects.filter(hideStatus=0)
    serializer_class = AccountTypeModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            AccountTypeModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class AccountPreferenceViewSet(viewsets.ModelViewSet):
    queryset = AccountPreferenceModel.objects.filter(hideStatus=0)
    serializer_class = AccountPreferenceModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            AccountPreferenceModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class ArnEntryViewSet(viewsets.ModelViewSet):
    queryset = ArnEntryModel.objects.filter(hideStatus=0)
    serializer_class = ArnEntryModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def countries(self, request):
        country_data = [{"code": code, "name": name} for code, name in list(countries)]
        return Response(country_data)

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            if pk == "0":
                serializer = ArnEntryModelSerializers(data=request.data)
            else:
                serializer = ArnEntryModelSerializers(instance=ArnEntryModel.objects.get(id=pk), data=request.data)
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
        user = request.user
        if user.is_authenticated:
            ArnEntryModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class AmcEntryViewSet(viewsets.ModelViewSet):
    queryset = AmcEntryModel.objects.filter(hideStatus=0)
    serializer_class = AmcEntryModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def countries(self, request):
        country_data = [{"code": code, "name": name} for code, name in list(countries)]
        return Response(country_data)

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            AmcEntryModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class FundViewSet(viewsets.ModelViewSet):
    queryset = FundModel.objects.filter(hideStatus=0)
    serializer_class = FundModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def by_amc(self, request):
        amc_id = request.query_params.get('amcId')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('pageSize', 50))
        search = request.query_params.get('search', '')

        if not amc_id:
            return Response({'code': 0, 'message': 'AMC ID is required'})

        funds = FundModel.objects.filter(hideStatus=0, fundAmcName_id=amc_id)

        if search:
            funds = funds.filter(fundName__icontains=search)

        funds = funds.order_by('fundName')

        paginator = Paginator(funds, page_size)

        try:
            funds_page = paginator.page(page)
        except Exception:
            return Response({'code': 0, 'message': 'Invalid page number'})

        serializer = FundModelSerializers(funds_page, many=True)

        return Response({
            'code': 1,
            'data': serializer.data,
            'message': 'Funds retrieved successfully',
            'total_pages': paginator.num_pages,
            'current_page': page,
            'total_items': paginator.count
        })

    @action(detail=False, methods=['GET'])
    def paginated_funds(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 100))
        search = request.query_params.get('search', '')
        amc_id = request.query_params.get('amc_id')

        queryset = self.get_queryset()

        if amc_id:
            queryset = queryset.filter(fundAmcName_id=amc_id)

        if search:
            queryset = queryset.filter(Q(fundName__icontains=search) | Q(schemeCode__icontains=search))

        start = (page - 1) * page_size
        end = start + page_size

        funds = queryset[start:end]
        total_count = queryset.count()

        serializer = self.get_serializer(funds, many=True)

        return Response({
            'results': serializer.data,
            'total_count': total_count,
            'page': page,
            'page_size': page_size
        })

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            if pk == "0":
                serializer = FundModelSerializers(FundModel.objects.filter(hideStatus=0).order_by('-id'),
                                                  many=True)
            else:
                serializer = FundModelSerializers(FundModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                                                  many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            if pk == "0":
                serializer = FundModelSerializers(data=request.data)
            else:
                try:
                    instance = FundModel.objects.get(id=pk)
                except FundModel.DoesNotExist:
                    return Response({'code': 0, 'message': "AMC not found"}, status=404)
                serializer = FundModelSerializers(instance=instance, data=request.data)
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
        user = request.user
        if user.is_authenticated:
            FundModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class AumEntryViewSet(viewsets.ModelViewSet):
    queryset = AumEntryModel.objects.filter(hideStatus=0)
    serializer_class = AumEntryModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            AumEntryModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class CommissionEntryViewSet(viewsets.ModelViewSet):
    queryset = CommissionEntryModel.objects.filter(hideStatus=0)
    serializer_class = CommissionEntryModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            CommissionEntryModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class AumYoyGrowthEntryViewSet(viewsets.ModelViewSet):
    queryset = AumYoyGrowthEntryModel.objects.filter(hideStatus=0)
    serializer_class = AumYoyGrowthEntryModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            if pk == "0":
                serializer = AumYoyGrowthEntryModelSerializers(data=request.data)
            else:
                serializer = AumYoyGrowthEntryModelSerializers(instance=AumYoyGrowthEntryModel.objects.get(id=pk),
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
        user = request.user
        if user.is_authenticated:
            AumYoyGrowthEntryModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class IndustryAumEntryViewSet(viewsets.ModelViewSet):
    queryset = IndustryAumEntryModel.objects.filter(hideStatus=0)
    serializer_class = IndustryAumEntryModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            IndustryAumEntryModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class GstEntryViewSet(viewsets.ModelViewSet):
    queryset = GstEntryModel.objects.filter(hideStatus=0)
    serializer_class = GstEntryModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            GstEntryModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class NavViewSet(viewsets.ModelViewSet):
    queryset = NavModel.objects.filter(hideStatus=0).order_by('-createdAt')
    serializer_class = NavModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def listing(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'code': 0, 'message': "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)

        page_size = int(request.query_params.get('page_size', 10))
        search = request.query_params.get('search', '')
        cursor = request.query_params.get('cursor')

        queryset = self.get_queryset().select_related('navFundName', 'navFundName__fundAmcName')

        if search:
            queryset = queryset.filter(
                Q(navFundName__fundAmcName__amcName__icontains=search) |
                Q(navFundName__fundName__icontains=search) |
                Q(nav__icontains=search)
            )

        if cursor:
            queryset = queryset.filter(id__lt=cursor)

        queryset = queryset.order_by('-id')[:page_size + 1]

        serializer = self.get_serializer(queryset[:page_size], many=True)

        data = {
            'code': 1,
            'data': serializer.data,
            'message': "Retrieved Successfully",
            'next_cursor': str(queryset[page_size].id) if len(queryset) > page_size else None
        }

        return Response(data)

    @action(detail=False, methods=['GET'])
    def total_count(self, request):
        total_count = self.get_queryset().count()
        return Response({'total_count': total_count})

    @action(detail=True, methods=['GET'])
    def list_for_update(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            try:
                instance = NavModel.objects.get(id=pk)
                serializer = NavModelSerializers(instance)
                return Response({'code': 1, 'data': serializer.data, 'message': "Retrieved Successfully"})
            except NavModel.DoesNotExist:
                return Response({'code': 0, 'message': "NAV not found"}, status=404)
        else:
            return Response({'code': 0, 'message': "Token is invalid"}, status=401)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            if pk == "0":
                serializer = NavModelSerializers(data=request.data)
            else:
                instance = NavModel.objects.get(id=pk)
                serializer = NavModelSerializers(instance=instance, data=request.data)

            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request", 'errors': serializer.errors}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=False, methods=['POST'])
    def fetch(self, request):
        user = request.user
        if user.is_authenticated:
            date = request.data.get('date')
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')

            try:
                if date:
                    call_command('fetch_nav_data', date=date)
                    message = f"NAV data fetched successfully for {date}"
                elif start_date and end_date:
                    call_command('fetch_nav_data', start_date=start_date, end_date=end_date)
                    message = f"Historic NAV data fetched successfully from {start_date} to {end_date}"
                else:
                    return Response({
                        'code': 0,
                        'message': "Invalid parameters. Provide either 'date' or both 'start_date' and 'end_date'."
                    }, status=status.HTTP_400_BAD_REQUEST)

                return Response({
                    'code': 1,
                    'message': message
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    'code': 0,
                    'message': f"Error fetching NAV data: {str(e)}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                'code': 0,
                'message': "Token is invalid"
            }, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            NavModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def get_nav_update_data(self, request, pk=None):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM get_nav_update_data(%s)", [pk])
                result = cursor.fetchone()

            if result:
                data = {
                    'navId': result[0],
                    'nav': float(result[1]),
                    'navDate': result[2].isoformat(),
                    'fundId': result[3],
                    'fundName': result[4],
                    'schemeCode': result[5],
                    'amcId': result[6],
                    'amcName': result[7]
                }
                return Response({'code': 1, 'data': data, 'message': 'NAV update data retrieved successfully'})
            else:
                return Response({'code': 0, 'message': 'NAV data not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'code': 0, 'message': f'Error retrieving NAV update data: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'])
    def funds_by_amc(self, request):
        amc_id = request.query_params.get('amc_id')
        if not amc_id:
            return Response({'error': 'AMC ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            funds = FundModel.objects.filter(fundAmcName_id=amc_id, hideStatus=0).values('id', 'fundName')
            return Response({'code': 1, 'data': list(funds), 'message': 'Funds retrieved successfully'})
        except Exception as e:
            return Response({'code': 0, 'message': f'Error retrieving funds: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IssueViewSet(viewsets.ModelViewSet):
    queryset = IssueModel.objects.filter(hideStatus=0)
    serializer_class = IssueModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            if pk == "0":
                queryset = IssueModel.objects.filter(hideStatus=0).order_by('-id')
            else:
                queryset = IssueModel.objects.filter(hideStatus=0, id=pk).order_by('-id')

            serializer = IssueModelSerializers(queryset, many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All Retrieved"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            if pk == "0":
                serializer = IssueModelSerializers(data=request.data)
            else:
                instance = IssueModel.objects.get(id=pk)
                serializer = IssueModelSerializers(instance=instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request", 'errors': serializer.errors}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            issue = IssueModel.objects.get(id=pk)
            issue.hideStatus = 1
            issue.save()
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class StatementViewSet(viewsets.ModelViewSet):
    queryset = StatementModel.objects.filter(hideStatus=0)
    serializer_class = StatementModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            StatementModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class CourierViewSet(viewsets.ModelViewSet):
    queryset = CourierModel.objects.filter(hideStatus=0)
    serializer_class = CourierModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            CourierModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class CourierFileViewSet(viewsets.ModelViewSet):
    queryset = CourierFileModel.objects.filter(hideStatus=0)
    serializer_class = CourierFileModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            files = CourierFileModel.objects.filter(courier_id=pk, hideStatus=0)
            serializer = CourierFileModelSerializers(files, many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All Files Retrieved"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            try:
                file = CourierFileModel.objects.get(id=pk)
                file.hideStatus = 1
                file.save()
                response = {'code': 1, 'message': "File Deleted Successfully"}
            except CourierFileModel.DoesNotExist:
                response = {'code': 0, 'message': "File not found"}
            except Exception as e:
                response = {'code': 0, 'message': str(e)}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class FormsViewSet(viewsets.ModelViewSet):
    queryset = FormsModel.objects.filter(hideStatus=0)
    serializer_class = FormsModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            if pk == "0":
                queryset = FormsModel.objects.filter(hideStatus=0).order_by('-id')
            else:
                queryset = FormsModel.objects.filter(hideStatus=0, id=pk).order_by('-id')

            serializer = FormsModelSerializers(queryset, many=True, context={'request': request})
            response = {'code': 1, 'data': serializer.data, 'message': "All Retrieved"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            FormsModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class MarketingViewSet(viewsets.ModelViewSet):
    queryset = MarketingModel.objects.filter(hideStatus=0)
    serializer_class = MarketingModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:  # Replace with proper token validation
            if pk == "0":
                queryset = self.queryset.order_by('-id')
            else:
                queryset = self.queryset.filter(id=pk).order_by('-id')

            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            data = serializer.data

            # Add full URL to marketingFile
            for item in data:
                if item['marketingFile']:
                    item['marketingFile'] = request.build_absolute_uri(item['marketingFile'])

            response = {'code': 1, 'data': data, 'message': "All Retrieved"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            MarketingModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def share_links(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            try:
                marketing = MarketingModel.objects.get(id=pk, hideStatus=0)
                file_url = request.build_absolute_uri(marketing.marketingFile.url)
                title = f"Check out this marketing material: {marketing.marketingType}"

                # WhatsApp sharing
                whatsapp_link = f"https://api.whatsapp.com/send?text={urllib.parse.quote(title + ' ' + file_url)}"

                # Telegram sharing
                telegram_link = f"https://t.me/share/url?url={urllib.parse.quote(file_url)}&text={urllib.parse.quote(title)}"

                # Facebook sharing
                facebook_link = f"https://www.facebook.com/sharer/sharer.php?u={urllib.parse.quote(file_url)}"

                response = {
                    'code': 1,
                    'data': {
                        'whatsapp': whatsapp_link,
                        'telegram': telegram_link,
                        'facebook': facebook_link,
                        'file_url': file_url,
                        'title': title,
                    },
                    'message': "Share links generated successfully"
                }
            except MarketingModel.DoesNotExist:
                response = {'code': 0, 'data': {}, 'message': "Marketing material not found"}
        else:
            response = {'code': 0, 'data': {}, 'message': "Unauthorized access"}

        return Response(response)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = TaskModel.objects.filter(hideStatus=0)
    serializer_class = TaskModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            TaskModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = EmployeeModel.objects.filter(hideStatus=0)
    serializer_class = EmployeeModelSerializers
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access these views

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            if pk == "0":
                queryset = EmployeeModel.objects.filter(hideStatus=0).order_by('-id')
            else:
                queryset = EmployeeModel.objects.filter(hideStatus=0, id=pk).order_by('-id')

            # Pass the request context to the serializer
            serializer = EmployeeModelSerializers(queryset, many=True, context={'request': request})
            response = {'code': 1, 'data': serializer.data, 'message': "All Retrieved"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def processing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            if pk == "0":
                serializer = EmployeeModelSerializers(data=request.data)
                if serializer.is_valid():
                    # Save new instance first
                    employee_instance = serializer.save()

                    # Hash the password if provided
                    raw_password = request.data.get('employeePassword', None)
                    if raw_password:
                        employee_instance.set_password(raw_password)
                        employee_instance.save()  # Save updated instance with hashed password
                    response = {'code': 1, 'message': "Done Successfully"}
                else:
                    response = {'code': 0, 'message': "Unable to Process Request", 'errors': serializer.errors}
            else:
                try:
                    employee_instance = EmployeeModel.objects.get(id=pk)
                except EmployeeModel.DoesNotExist:
                    return Response({'code': 0, 'message': "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

                serializer = EmployeeModelSerializers(instance=employee_instance, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()  # Save instance first

                    # Hash the password if provided
                    raw_password = request.data.get('employeePassword', None)
                    if raw_password:
                        employee_instance.set_password(raw_password)
                        employee_instance.save()  # Save updated instance with hashed password
                    response = {'code': 1, 'message': "Done Successfully"}
                else:
                    response = {'code': 0, 'message': "Unable to Process Request", 'errors': serializer.errors}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def update_password(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            try:
                employee = EmployeeModel.objects.get(id=pk)
                new_password = request.data.get('newPassword')
                if new_password:
                    employee.set_password(new_password)
                    employee.save()
                    return Response({'code': 1, 'message': "Password updated successfully"})
                else:
                    return Response({'code': 0, 'message': "New password is required"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except EmployeeModel.DoesNotExist:
                return Response({'code': 0, 'message': "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'code': 0, 'message': "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            EmployeeModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = ClientModel.objects.filter(hideStatus=0)
    serializer_class = ClientModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def countries(self, request):
        country_data = [{"code": code, "name": name} for code, name in list(countries)]
        return Response(country_data)

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
                    else:
                        logger.error(f"Client serializer errors: {client_serializer.errors}")
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
                    file_instance, created = ClientUploadFileModel.objects.get_or_create(
                        clientUploadFileId=client_instance)
                    if upload_files_data:
                        for field_name, file_data in upload_files_data.items():
                            if file_data:
                                if isinstance(file_data, str) and file_data.startswith('data:'):
                                    format, imgstr = file_data.split(';base64,')
                                    ext = format.split('/')[-1]
                                    data = ContentFile(base64.b64decode(imgstr), name=f'{field_name}.{ext}')
                                elif isinstance(file_data,
                                                dict) and 'name' in file_data and 'content' in file_data:
                                    ext = file_data['name'].split('.')[-1]
                                    data = ContentFile(base64.b64decode(file_data['content']),
                                                       name=file_data['name'])
                                else:
                                    logger.warning(
                                        f"Unexpected file data format for {field_name}: {type(file_data)}")
                                    continue
                                setattr(file_instance, field_name, data)
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
                    guardian_instance, created = ClientGuardianModel.objects.get_or_create(
                        clientGuardianId=client_instance)
                    guardian_serializer = ClientGuardianModelSerializers(instance=guardian_instance, data=guardian_data)
                    if guardian_serializer.is_valid():
                        guardian_serializer.save(clientGuardianId=client_instance)
                    else:
                        return Response(
                            {'code': 0, 'message': "Invalid guardian data", 'errors': guardian_serializer.errors})

                    # Process attorney details
                    attorney_data = request.data.get('attorneyJson', {})
                    attorney_instance, created = ClientPowerOfAttorneyModel.objects.get_or_create(
                        clientPowerOfAttorneyId=client_instance)
                    attorney_serializer = ClientPowerOfAttorneyModelSerializers(instance=attorney_instance,
                                                                                data=attorney_data)
                    if attorney_serializer.is_valid():
                        attorney_serializer.save(clientPowerOfAttorneyId=client_instance)
                    else:
                        return Response(
                            {'code': 0, 'message': "Invalid attorney data", 'errors': attorney_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

                return Response({'code': 1, 'message': "Client data processed successfully"},
                                status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error processing client data: {e}")
                return Response({'code': 0, 'message': "An error occurred while processing the data"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'code': 0, 'message': "Authentication token missing"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        try:
            user = request.user
            if not user.is_authenticated:
                return Response({'code': 0, 'message': "Unauthorized access"}, status=401)

            with transaction.atomic():
                client = ClientModel.objects.get(id=pk)

                # Update hideStatus for the main client
                client.hideStatus = '1'
                client.save()

                # Update hideStatus for related models
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
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            ClientFamilyDetailModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class ClientChildrenDetailViewSet(viewsets.ModelViewSet):
    queryset = ClientChildrenDetailModel.objects.filter(hideStatus=0)
    serializer_class = ClientChildrenDetailModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            ClientChildrenDetailModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class ClientPresentAddressViewSet(viewsets.ModelViewSet):
    queryset = ClientPresentAddressModel.objects.filter(hideStatus=0)
    serializer_class = ClientPresentAddressModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            ClientPresentAddressModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class ClientPermanentAddressViewSet(viewsets.ModelViewSet):
    queryset = ClientPermanentAddressModel.objects.filter(hideStatus=0)
    serializer_class = ClientPermanentAddressModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            ClientPermanentAddressModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class ClientOfficeAddressViewSet(viewsets.ModelViewSet):
    queryset = ClientOfficeAddressModel.objects.filter(hideStatus=0)
    serializer_class = ClientOfficeAddressModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            ClientOfficeAddressModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class ClientOverseasAddressViewSet(viewsets.ModelViewSet):
    queryset = ClientOverseasAddressModel.objects.filter(hideStatus=0)
    serializer_class = ClientOverseasAddressModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            ClientOverseasAddressModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class ClientNomineeViewSet(viewsets.ModelViewSet):
    queryset = ClientNomineeModel.objects.filter(hideStatus=0)
    serializer_class = ClientNomineeModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            ClientNomineeModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class ClientMedicalInsuranceViewSet(viewsets.ModelViewSet):
    queryset = ClientMedicalInsuranceModel.objects.filter(hideStatus=0)
    serializer_class = ClientMedicalInsuranceModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            ClientMedicalInsuranceModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class ClientTermInsuranceViewSet(viewsets.ModelViewSet):
    queryset = ClientTermInsuranceModel.objects.filter(hideStatus=0)
    serializer_class = ClientTermInsuranceModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            ClientTermInsuranceModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class ClientUploadFileViewSet(viewsets.ModelViewSet):
    queryset = ClientUploadFileModel.objects.filter(hideStatus=0)
    serializer_class = ClientUploadFileModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            ClientUploadFileModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class ClientBankViewSet(viewsets.ModelViewSet):
    queryset = ClientBankModel.objects.filter(hideStatus=0)
    serializer_class = ClientBankModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            ClientBankModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class ClientTaxViewSet(viewsets.ModelViewSet):
    queryset = ClientTaxModel.objects.filter(hideStatus=0)
    serializer_class = ClientTaxModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            ClientTaxModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class ClientPowerOfAttorneyViewSet(viewsets.ModelViewSet):
    queryset = ClientPowerOfAttorneyModel.objects.filter(hideStatus=0)
    serializer_class = ClientPowerOfAttorneyModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
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
        user = request.user
        if user.is_authenticated:
            if pk == "0":
                serializer = ClientPowerOfAttorneyModelSerializers(data=request.data)
            else:
                instance = ClientPowerOfAttorneyModel.objects.get(id=pk)
                serializer = ClientPowerOfAttorneyModelSerializers(instance=instance, data=request.data)

            if serializer.is_valid():
                if 'clientPowerOfAttorneyUpload' in request.FILES:
                    file = request.FILES['clientPowerOfAttorneyUpload']
                    serializer.validated_data['clientPowerOfAttorneyUpload'] = file

                serializer.save()
                response = {'code': 1, 'message': "Done Successfully"}
            else:
                response = {'code': 0, 'message': "Unable to Process Request", 'errors': serializer.errors}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            ClientPowerOfAttorneyModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)


class DailyEntryViewSet(viewsets.ModelViewSet):
    queryset = DailyEntryModel.objects.filter(hideStatus=0)
    serializer_class = DailyEntryModelSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def get_client_details(self, request):
        search_term = request.query_params.get('search_term')
        if not search_term:
            return Response({'code': 0, 'message': 'Search term is required'})

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM get_client_details(%s)", [search_term])
            columns = [col[0] for col in cursor.description]
            client = cursor.fetchone()

        if client:
            client_data = dict(zip(columns, client))
            return Response({'code': 1, 'data': client_data, 'message': 'Client details retrieved successfully'})
        else:
            return Response({'code': 0, 'message': 'Client not found'})

    @action(detail=False, methods=['GET'])
    def get_funds_by_amc(self, request):
        amc_id = request.query_params.get('amc_id')
        if not amc_id:
            return Response({'code': 0, 'message': 'AMC ID is required'})

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM get_funds_by_amc(%s)", [amc_id])
            funds = [{'id': row[0], 'fundName': row[1], 'schemeCode': row[2]} for row in cursor.fetchall()]

        return Response({'code': 1, 'data': funds, 'message': 'Funds retrieved successfully'})

    @action(detail=False, methods=['POST'])
    @transaction.atomic
    def processing(self, request):
        user = request.user
        if user.is_authenticated:
            data = request.data
            try:
                # Get or create ClientModel instance
                client, _ = ClientModel.objects.get_or_create(
                    clientPanNo=data['dailyEntryClientPanNumber'],
                    defaults={
                        'clientName': data['dailyEntryClientName'],
                        'clientPhone': data['dailyEntryClientMobileNumber']
                    }
                )

                # Get related objects
                fund_house = AmcEntryModel.objects.get(id=data['dailyEntryFundHouse'])
                fund = FundModel.objects.get(id=data['dailyEntryFundName'])
                issue_type = IssueTypeModel.objects.get(id=data['dailyEntryIssueType'])

                # Create DailyEntryModel instance
                daily_entry = DailyEntryModel.objects.create(
                    applicationDate=datetime.strptime(data['applicationDate'], '%Y-%m-%d').date(),
                    dailyEntryClientPanNumber=client,
                    dailyEntryClientName=client,
                    dailyEntryClientFolioNumber=data['clientFolioNumber'],
                    dailyEntryClientMobileNumber=client,
                    dailyEntryFundHouse=fund_house,
                    dailyEntryFundName=fund,
                    dailyEntryAmount=data['amount'],
                    dailyEntryClientChequeNumber=data['clientChequeNumber'],
                    dailyEntryIssueType=issue_type,
                    dailyEntrySipDate=datetime.strptime(data['sipDate'], '%Y-%m-%d').date() if data[
                        'sipDate'] else None,
                    dailyEntryStaffName=data['staffName'],
                    dailyEntryTransactionAddDetails=data.get('transactionAddDetail', '')
                )

                # Calculate issue resolution date
                issue_resolution_date = daily_entry.applicationDate + timedelta(days=issue_type.estimatedIssueDay)

                # Create IssueModel instance
                issue = IssueModel.objects.create(
                    issueClientName=client,
                    issueType=issue_type,
                    issueDate=daily_entry.applicationDate,
                    issueResolutionDate=issue_resolution_date,
                    issueDescription=data.get('transactionAddDetail', '')
                )

                return Response({
                    'code': 1,
                    'message': 'Daily entry and issue created successfully',
                    'daily_entry_id': daily_entry.id,
                    'issue_id': issue.id
                })
            except Exception as e:
                transaction.set_rollback(True)
                return Response({'code': 0, 'message': f'Failed to create daily entry and issue: {str(e)}'})
        else:
            return Response({'code': 0, 'message': 'Token is invalid'})

    @action(detail=True, methods=['GET'])
    def listing(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            if pk == "0":
                serializer = DailyEntryModelSerializers(
                    DailyEntryModel.objects.filter(hideStatus=0).order_by('-id'),
                    many=True)
            else:
                serializer = DailyEntryModelSerializers(
                    DailyEntryModel.objects.filter(hideStatus=0, id=pk).order_by('-id'),
                    many=True)
            response = {'code': 1, 'data': serializer.data, 'message': "All  Retried"}
        else:
            response = {'code': 0, 'data': [], 'message': "Token is invalid"}
        return Response(response)

    @action(detail=True, methods=['GET'])
    def deletion(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            DailyEntryModel.objects.filter(id=pk).update(hideStatus=1)
            response = {'code': 1, 'message': "Done Successfully"}
        else:
            response = {'code': 0, 'message': "Token is invalid"}
        return Response(response)
