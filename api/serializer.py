from rest_framework import serializers
from api import models

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.UserInfo
        fields='__all__'


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Device
        fields='__all__'



class ShujuSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Shuju
        fields='__all__'
