# models
from ..Models.driver_model import DriverModel

# serializers
from ..Serializers.driver_serializer import DriverSerializer

# generic APIs
from rest_framework.generics import UpdateAPIView, ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView

# API authentication permissions
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

# rest framework
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

# helper functions
# from ..helper_functions.functions import get_user_id_from_request

# swagger imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator

import csv
import codecs
from io import TextIOWrapper

@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=['Driver-endpoints']
    ),
)
class CreateDriver(CreateAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = DriverModel.objects.all()
    serializer_class = DriverSerializer

@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        tags=['Driver-endpoints']
    ),
)
class UpdateDriver(UpdateAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = DriverModel.objects.all()
    serializer_class = DriverSerializer
    http_method_names = ['patch']

@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=['Driver-endpoints']
    ),
)
class RetrieveDriver(RetrieveAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = DriverModel.objects.all()
    serializer_class = DriverSerializer


@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        tags=['Driver-endpoints']
    ),
)
class DestroyDriver(DestroyAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = DriverModel.objects.all()
    serializer_class = DriverSerializer


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=['Driver-endpoints']
    ),
)
class ListDriver(ListAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = DriverModel.objects.all()
    serializer_class = DriverSerializer
