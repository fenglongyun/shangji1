from rest_framework import serializers
from api import models

class CompanysSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Company
        fields='__all__'



class DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Department
        fields='__all__'

class CompanysDepartmentsSerializer(serializers.ModelSerializer):
    department_set=DepartmentsSerializer(read_only=True,many=True)
    class Meta:
        model=models.Company
        fields=['id','company','department_set']



class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.UserInfo
        fields='__all__'

class MenuSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=models.Menu
        fields='__all__'

class MenutreeSerializer(serializers.ModelSerializer):
    subs=MenuSerializer(read_only=True,many=True)
    class Meta:
        model=models.Menu
        fields=['id','name','level','subs']


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Device
        fields='__all__'



class ShujuSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Shuju
        fields='__all__'

class BaoJingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=models.Shuju
        fields=['id','devtype','alarmnum','devnum']