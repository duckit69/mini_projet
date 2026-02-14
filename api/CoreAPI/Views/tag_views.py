# models
from ..Models.tag_model import TagModel

# serializers
from ..Serializers.tag_serializer import TagSerializer

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
        tags=['Tag-endpoints']
    ),
)
class CreateTag(CreateAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = TagModel.objects.all()
    serializer_class = TagSerializer

@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        tags=['Tag-endpoints']
    ),
)
class UpdateTag(UpdateAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = TagModel.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['patch']

@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=['Tag-endpoints']
    ),
)
class RetrieveTag(RetrieveAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = TagModel.objects.all()
    serializer_class = TagSerializer


@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        tags=['Tag-endpoints']
    ),
)
class DestroyTag(DestroyAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = TagModel.objects.all()
    serializer_class = TagSerializer


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=['Tag-endpoints']
    ),
)
class ListTag(ListAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = TagModel.objects.all()
    serializer_class = TagSerializer
