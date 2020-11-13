from rest_framework.views import APIView
from rest_framework.response import Response
from api import models
from api.auth import JwtAuth
from api.mypermission import MyPermission1
from api import serializer
import json

class UnauthorizedUsers(APIView):
    authentication_classes=[JwtAuth]
    permission_classes=[MyPermission1]
    #后台获取未经授权的用户列表
    def get(self,request,*args, **kwargs):
        queryset=models.UserInfo.objects.filter(category='0').all()
        ser=serializer.UserInfoSerializer(queryset,many=True)
        return Response(ser.data,headers={"Access-Control-Allow-Origin":"*"})
        
        
class AuthorizedUsers(APIView):
    authentication_classes=[JwtAuth]
    permission_classes=[MyPermission1]
    #后台获取已经授权的用户列表
    def get(self,request,*args, **kwargs):
        queryset=models.UserInfo.objects.filter(category='1').all()
        ser=serializer.UserInfoSerializer(queryset,many=True)
        return Response(ser.data,headers={"Access-Control-Allow-Origin":"*"})


class Menulist(APIView):
    authentication_classes=[JwtAuth]
    permission_classes=[MyPermission1]
    # 后台获取前台菜单列表
    def get(self,request,*args, **kwargs):
        queryset=models.Menu.objects.all()
        ser=serializer.MenuSerializer(queryset,many=True)
        return Response(ser.data,headers={"Access-Control-Allow-Origin":"*"})

class Menutree(APIView):
    authentication_classes=[JwtAuth]
    permission_classes=[MyPermission1]
    # 后台获取前台菜单列表
    def get(self,request,*args, **kwargs):
        queryset=models.Menu.objects.all()
        ser=serializer.MenuSerializer(queryset,many=True)
        list1=ser.data
        for x in reversed(list1):
            x['children']=[]
            for y in reversed(list1):
                if y['parent']==x['id']:
                    x['children'].append(y)
        list2=[list1[0],list1[1],list1[2]]
        return Response(list2,headers={"Access-Control-Allow-Origin":"*"})