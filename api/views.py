from rest_framework.views import APIView
from rest_framework.response import Response
from api import models
from django.forms.models import model_to_dict
from api import serializer
from rest_framework.pagination import PageNumberPagination
from api.auth import JwtAuth
from api.mypermission import MyPermission1
from api.utils.jwt_auth import create_token
from api.mypagination import MyPagination
from django.db.models.aggregates import Count ,Max
import requests
import json
from django.db.models import Q



    
    
# Create your views here.
class Login(APIView):
    def post(self,request,*args, **kwargs):
        user=request.data.get('username')
        pwd=request.data.get('password')
        user_obj=models.UserInfo.objects.filter(username=user,password=pwd).first()
        if not user_obj:
            return Response({'code':0,'msg':'用户名或密码错误'},headers={'Access-Control-Allow-Origin':'*'})
        elif user_obj.category=='0':
            return Response({'code':0,'msg':'该用户未经授权，无法登录'},headers={'Access-Control-Allow-Origin':'*'})
        token=create_token({'id':user_obj.pk,'username':user_obj.username,'company':user_obj.company,'userrole':user_obj.userrole},1)
        return Response({'code':1,'msg':'登录成功','userrole':user_obj.userrole,'token':token},headers={'Access-Control-Allow-Origin':'*'})



class Userinfo(APIView):
    authentication_classes=[JwtAuth]
    #获取个人信息接口
    def get(self,request,*args,**kwargs):
        userinfo_id=request.user['id']
        queryset=models.UserInfo.objects.filter(id=userinfo_id).first()
        ser=serializer.UserInfoSerializer(queryset)
        return Response(ser.data,headers={'Access-Control-Allow-Origin':'*'})

    #修改个人信息接口
    def put(self,request ,*args, **kwagrs):
        userinfo_id=request.user['id']
        data=request.data
        if 'username' in data:
            data.pop('username')
        models.UserInfo.objects.filter(id=userinfo_id).update(**data)
        return Response('更新成功',headers={"Access-Control-Allow-Origin":"*"})                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             




class Departments(APIView):
    authentication_classes=[JwtAuth]
    def get(self,request,*args, **kwargs):
        #获取本公司所有部门接口
        mycompany=request.user['company']
        queryset=models.Company.objects.filter(company=mycompany).first()
        departments=queryset.department_set.values('id','department')
        return Response(departments,headers={"Access-Control-Allow-Origin":"*"})

    def post(self,request,*args, **kwargs):
        mycompany=request.user['company']
        mycompany_iddict=models.Company.objects.filter(company=mycompany).values('id').first()
        mycompany_id=mycompany_iddict['id']
        department=request.data.get('department')
        queryset=models.Department.objects.filter(company_id=mycompany_id,department=department)
        if queryset:
             return Response({'code':0,'msg':'部门已存在，添加失败'},headers={"Access-Control-Allow-Origin":"*"})
        models.Department.objects.create(department=department,company_id=mycompany_id)
        return Response({'code':1,'msg':'部门添加成功'},headers={"Access-Control-Allow-Origin":"*"})

    def delete(self,request,*args, **kwargs):
        mycompany=request.user['company']
        pk=kwargs.get('pk')
        mycompany_iddict=models.Company.objects.filter(company=mycompany).values('id').first()
        mycompany_id=mycompany_iddict['id']
        queryset=models.Department.objects.filter(company_id=mycompany_id,id=pk).first()
        if not queryset:
            return Response({'code':0,'msg':'无此部门，删除失败'},headers={"Access-Control-Allow-Origin":"*"})
        queryset.delete()
        return Response({'code':1,'msg':'部门删除成功'},headers={"Access-Control-Allow-Origin":"*"})



class UserList(APIView):
    authentication_classes=[JwtAuth]
    permission_classes=[MyPermission1]
    #前台管理员获取本公司所有用户信息
    def get(self,request,*args, **kwargs):
        pk=kwargs.get('pk')
        mycompany=request.user['company']
        mydepartment=request.GET.get('department')
        myusername=request.GET.get('username')
        if not pk:
            if  mydepartment and myusername:
                queryset=models.UserInfo.objects.filter(company=mycompany,department=mydepartment,username=myusername).all().order_by('id')
            elif mydepartment:
                queryset=models.UserInfo.objects.filter(company=mycompany,department=mydepartment).all().order_by('id')
            elif myusername:
                queryset=models.UserInfo.objects.filter(company=mycompany,username=myusername).all().order_by('id')
            else:
                queryset=models.UserInfo.objects.filter(company=mycompany).all().order_by('id')
            page_obj=MyPagination()
            page_data=page_obj.paginate_queryset(queryset,request,self)
            ser=serializer.UserInfoSerializer(page_data,many=True)
            return page_obj.get_paginated_response(ser.data)
        else:
            queryset=models.UserInfo.objects.filter(id=pk).first()
            ser=serializer.UserInfoSerializer(queryset)
            return Response(ser.data,headers={"Access-Control-Allow-Origin":"*"})
        

    def post(self,request,*args, **kwargs):
        data=request.data
        queryset=models.UserInfo.objects.filter(username=data['username']).first()
        if queryset:
            return Response({'code':0,'msg':'用户添加失败，用户已存在'},headers={"Access-Control-Allow-Origin":"*"})
        data['company']=mycompany
        models.UserInfo.objects.create(**data)
        return Response({'code':1,'msg':'用户添加成功'},headers={"Access-Control-Allow-Origin":"*"})

    def put(self,request,*args, **kwargs):
        pk=kwargs.get('pk')
        data=request.data
        if 'username' in data:
            data.pop('username')
        models.UserInfo.objects.filter(id=pk).update(**request.data)
        return Response({'code':1,'msg':'更新成功'},headers={'Access-Control-Allow-Origin':'*'})

    def delete(self,request,*args, **kwargs):
        pk=kwargs.get('pk')
        models.UserInfo.objects.filter(id=pk).delete()
        return Response({'code':1,'msg':'删除成功'},headers={'Access-Control-Allow-Origin':'*'})


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
    # 后台获取菜单列表
    def get(self,request,*args, **kwargs):
        queryset=models.Menu.objects.all()
        ser=serializer.MenuSerializer(queryset,many=True)
        return Response(ser.data,headers={"Access-Control-Allow-Origin":"*"})


class Device(APIView):
    authentication_classes=[JwtAuth]
    def get(self,request ,*args, **kwagrs):
        pk=kwagrs.get('pk')
        userinfo_id=request.user['id'] 
        if not pk: 
            return Response('请求参数错误',headers={"Access-Control-Allow-Origin":"*"})
        elif pk=='all':
            if userinfo_id==1:
                queryset=models.Device.objects.all().order_by('id')
            else:
                queryset=models.Device.objects.filter(userinfo_id=userinfo_id).all().order_by('id')
            page_obj=MyPagination()
            page_data=page_obj.paginate_queryset(queryset,request,self)        
            ser=serializer.DeviceSerializer(page_data,many=True)
            return page_obj.get_paginated_response(ser.data)
        else:
            if userinfo_id==1:
                queryset=models.Device.objects.filter(id=pk).first()
            else:
                queryset=models.Device.objects.filter(userinfo_id=userinfo_id, id=pk).first()
            if not queryset:
                return Response({'code':0,'msg':'请求参数错误'}, headers={"Access-Control-Allow-Origin":"*"})
            ser=serializer.DeviceSerializer(queryset,many=False)
            return Response(ser.data,headers={"Access-Control-Allow-Origin":"*"})

    def post(self,request ,*args, **kwagrs):
        data=request.data
        queryset=models.Device.objects.filter(Q(devnum=data['devnum']) | Q(devtype=data['devtype'])).all()
        if queryset:
            return Response({'code':0,'msg':'设备添加失败，资产编号或IOT设备编号有误'},headers={"Access-Control-Allow-Origin":"*"})
        userinfo_id=request.user['id']
        data['userinfo_id']=userinfo_id
        models.Device.objects.create(**data)
        return Response({'code':0,'msg':'设备添加成功'},headers={"Access-Control-Allow-Origin":"*"})

    def put(self,request ,*args, **kwagrs):
        pk=kwagrs.get('pk')
        userinfo_id=request.user['id']
        data=request.data
        if userinfo_id==1:
            dev_obj=models.Device.objects.filter(id=pk).first()
        else:
            dev_obj=models.Device.objects.filter(userinfo_id=userinfo_id, id=pk).first()
        if not dev_obj:
            return Response({'code':0,'msg':'设备id参数错误，更新失败'},headers={"Access-Control-Allow-Origin":"*"})
        dev_obj.update(**data)
        return Response({'code':1,'msg':'更新成功'},headers={"Access-Control-Allow-Origin":"*"}) 

    def delete(self,request ,*args, **kwagrs):
        pk=kwagrs.get('pk')
        userinfo_id=request.user['id']
        if userinfo_id==1:
            dev_obj=models.Device.objects.filter(id=pk).first()
        else:
            dev_obj=models.Device.objects.filter(userinfo_id=userinfo_id, id=pk).first()
        if not dev_obj:
            return Response({'code':0,'msg':'设备id参数错误，删除失败'},headers={"Access-Control-Allow-Origin":"*"})
        models.Device.objects.filter(id=pk).delete()
        return Response({'code':1,'msg':'删除成功'},headers={"Access-Control-Allow-Origin":"*"})




class Cncstates(APIView):
    authentication_classes=[JwtAuth]
    #统计个人所有设备的状态
    def get(self,request,*args, **kwargs):
        userinfo_id=request.user['id']
        if userinfo_id==1:
            dev_objs=models.Device.objects.all().values("cncstate").annotate(Count('id'))
        else:
            dev_objs=models.Device.objects.filter(userinfo_id=userinfo_id).values("cncstate").annotate(Count('id'))
        return Response({'code':1,'msg':dev_objs},headers={"Access-Control-Allow-Origin":"*"})


class FailureWarning(APIView):
    authentication_classes=[JwtAuth]
    def get(self,request,*args, **kwargs):
        userinfo_id=request.user['id']
        if userinfo_id==1:
            queryset=models.Shuju.objects.values('devtype').annotate(max1=Max('id'))
            b=[y['max1'] for y in queryset]
            queryset=models.Shuju.objects.filter(id__in=b).all().values('id','devtype','alarmnum')
            return Response(queryset,headers={"Access-Control-Allow-Origin":"*"})
        else:
            devtypes=models.Device.objects.filter(userinfo_id=userinfo_id).all().values('devtype')
            a=[x['devtype'] for x in devtypes]
            queryset=models.Shuju.objects.filter(devtype__in=a).values('devtype').annotate(max1=Max('id'))
            b=[y['max1'] for y in queryset]
            queryset=models.Shuju.objects.filter(id__in=b).all().values('id','devtype','alarmnum')
            return Response(queryset,headers={"Access-Control-Allow-Origin":"*"})

class Cameraaddress(APIView):
    authentication_classes=[JwtAuth]
    #获取摄像头监控地址
    def get(self,request,*args, **kwargs):
        pk=kwargs.get('pk')
        userinfo_id=request.user['id']
        if userinfo_id==1:
            dev_obj=models.Device.objects.filter(id=pk).first()
        else:
            dev_obj=models.Device.objects.filter(userinfo_id=userinfo_id,id=pk).first()
        if not dev_obj:
            return Response({'code':0,'msg':'请求参数错误'},headers={"Access-Control-Allow-Origin":"*"})
        cameranum=dev_obj.cameranum
        payload={
            'appKey':'dbfb66c28cc04f888fc462fff12ff5fb',
            'appSecret':'16f9647802a4391bdaf3b1871355d76f'
            }
        res=requests.post('http://open.ys7.com/api/lapp/token/get',data=payload)
        json_res=json.loads(res.text)
        camera_address='https://open.ys7.com/ezopen/h5/iframe?url=ezopen://open.ys7.com/'+cameranum+'/1.hd.live&autoplay=1&accessToken=' + json_res['data']['accessToken']
        return Response({'code':1,'msg':camera_address},headers={"Access-Control-Allow-Origin":"*"})




class Shuju(APIView):
    
    def get(self,request ,*args, **kwagrs):
        devtype=kwagrs.get('devtype')
        if not devtype:
            return Response('请求参数错误',headers={"Access-Control-Allow-Origin":"*"})
        else:
            queryset=models.Shuju.objects.filter(devtype=devtype).order_by('-id').first()
            ser=serializer.ShujuSerializer(queryset)
            return Response(ser.data,headers={"Access-Control-Allow-Origin":"*"})

    # def post(self,request ,*args, **kwagrs):
    #     data=request.data
    #     models.Shuju.objects.create(**data)
    #     return Response('添加成功')

    # def put(self,request ,*args, **kwagrs):
    #     pk=kwagrs.get('pk')
    #     models.Shuju.objects.filter(id=pk).update(**request.data)
    #     return Response('更新成功') 

    # def patch(self,request ,*args, **kwagrs):
    #     pk=kwagrs.get('pk')
        
    #     return Response('局部更新成功')

    # def delete(self,request ,*args, **kwagrs):
    #     pk=kwagrs.get('pk')
    #     models.Shuju.objects.filter(id=pk).delete()
    #     return Response('删除成功')