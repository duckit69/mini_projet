# models
from ..Models.mission_model import MissionModel

# serializers
from ..Serializers.mission_serializer import MissionSerializer

# filters
from ..Filters.mission_filter import MissionFilter

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
        tags=['Mission-endpoints']
    ),
)
class CreateMission(CreateAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = MissionModel.objects.all()
    serializer_class = MissionSerializer

@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        tags=['Mission-endpoints']
    ),
)
class UpdateMission(UpdateAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = MissionModel.objects.all()
    serializer_class = MissionSerializer
    http_method_names = ['patch']

@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=['Mission-endpoints']
    ),
)
class RetrieveMission(RetrieveAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = MissionModel.objects.all()
    serializer_class = MissionSerializer


@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        tags=['Mission-endpoints']
    ),
)
class DestroyMission(DestroyAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = MissionModel.objects.all()
    serializer_class = MissionSerializer


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=['Mission-endpoints']
    ),
)
class ListMission(ListAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = MissionModel.objects.all()
    serializer_class = MissionSerializer
    filterset_class = MissionFilter
