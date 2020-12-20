from rest_framework.views import APIView
from rest_framework.response import Response
from api import models
from api.auth import JwtAuth
from api.mypermission import MyPermission1
from api import serializer
from shangji import settings
import json
import os