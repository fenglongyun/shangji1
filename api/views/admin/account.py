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
        
class UnauthorizedUser(APIView):
    authentication_classes=[JwtAuth]
    permission_classes=[MyPermission1]
    ###删除一个未授权用户
    def delete(self,request,*args, **kwargs):
        pk = kwargs.get('pk')
        models.UserInfo.objects.filter(id=pk).delete()
        return Response({
            "code" : 3000,
            "msg" : '删除成功',
        })

class AuthorizedUsers(APIView):
    authentication_classes=[JwtAuth]
    permission_classes=[MyPermission1]
    #后台获取已经授权的用户列表
    def get(self,request,*args, **kwargs):
        res = request.GET.get("username")
        if res:
            #模糊搜索
            queryset=models.UserInfo.objects.filter(category='1',username__contains=res).all()
        else:
            queryset=models.UserInfo.objects.filter(category='1').all()
        ser=serializer.UserInfoSerializer(queryset,many=True)
        return Response(ser.data,headers={"Access-Control-Allow-Origin":"*"})

class AuthorizedUser(APIView):
    authentication_classes=[JwtAuth]
    permission_classes=[MyPermission1]
    #修改一个用户信息
    def put(self,request,*args, **kwargs):
        pk = kwargs.get('pk')
        data = request.data
        models.UserInfo.objects.filter(id = pk).update(**data)
        return Response({
            "code" : 2000,
            "msg" : "修改成功"
        })
    ###删除一个授权用户
    def delete(self,request,*args, **kwargs):
        pk = kwargs.get('pk')
        models.UserInfo.objects.filter(id=pk).delete()
        return Response({
            "code" : 3000,
            "msg" : '删除成功',
        })
    
    #新增一个授权用户
    def post(self,request,*args, **kwargs):
        info = request.data.get("info")
        if models.UserInfo.objects.filter(username = info['username']).all():
            return Response({
                "code" : 0,
                "msg" : "新增失败，账号已存在"
            })
        obj = models.UserInfo.objects.create(**info)
        auth = request.data.get("auth")
        user_menu_objs=[]
        for x in auth:
            user_menu_objs.append(models.UserInfo_Menu(userinfo_id=obj.id,menu_id=x))
        models.UserInfo_Menu.objects.bulk_create(user_menu_objs)
        return Response({
            "code" : 1,
            "msg" : "添加成功",
        })

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
        queryset=models.Menu.objects.all().order_by('id')
        ser=serializer.MenuSerializer(queryset,many=True)
        list1=ser.data
        for x in reversed(list1):
            x['children']=[]
            for y in reversed(list1):
                if y['parent']==x['id']:
                    x['children'].append(y)
        list2 = filter(lambda e:not e["parent"],list1)
        return Response(list2,headers={"Access-Control-Allow-Origin":"*"})

class UserAuthorization(APIView):
    authentication_classes=[JwtAuth]
    permission_classes=[MyPermission1]
    #后台授权用户登录并赋予菜单权限
    def put(self,request,*args, **kwargs):
        pk=kwargs.get('pk')
        user_obj=models.UserInfo.objects.filter(id=pk).first()
        user_obj.category=1
        user_obj.userrole="2"
        user_obj.save()
        data=request.data
        user_menu_objs=[]
        for x in data:
            user_menu_objs.append(models.UserInfo_Menu(userinfo_id=pk,menu_id=x))
        models.UserInfo_Menu.objects.bulk_create(user_menu_objs)
        return Response({'code':1,'msg':'授权成功'},headers={"Access-Control-Allow-Origin":"*"})
    
class UserMenus(APIView):
    authentication_classes=[JwtAuth]
    permission_classes=[MyPermission1]
    #后台获取某用户菜单权限id列表
    def get(self,request,*args, **kwargs):
        pk=kwargs.get('pk')
        menus_list=models.UserInfo_Menu.objects.filter(userinfo_id=pk).values('menu_id')
        c=[x['menu_id'] for x in menus_list]
        return Response(c,headers={"Access-Control-Allow-Origin":"*"})
    
    #后台修改某用户菜单权限
    def put(self,request,*args, **kwargs):
        pk=kwargs.get('pk')
        objs=models.UserInfo_Menu.objects.filter(userinfo_id=pk).all()
        objs.delete()
        data=request.data
        user_menu_objs=[]
        for x in data:
            user_menu_objs.append(models.UserInfo_Menu(userinfo_id=pk,menu_id=x))
        models.UserInfo_Menu.objects.bulk_create(user_menu_objs)
        return Response({'code':1,'msg':'菜单权限修改成功'},headers={"Access-Control-Allow-Origin":"*"})
