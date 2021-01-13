from  rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from api.serializer import StateDevSerializer
from api.models import Device
from api.auth import JwtAuth
from api.mypagination import MyPagination
from api.utils.fileupload import fileupload
class UpdateDevPic(APIView):
    """ 修改设备图片接口 """
    #authentication_classes = [JwtAuth]
    def put(self, request, *args, **kwargs):
        dev_id =kwargs.get('pk')
        file =request.data.get('file')
        if not file:
            return Response({'code':'0', 'msg':'上传失败'})
        else:
            newfilename = fileupload(file, 'devpic')
            fileaddress = '/devpic/'+ newfilename 
            Device.objects.filter(id = dev_id).update(cncphotos=fileaddress)
            return Response({'code':'1', 'msg':'上传成功','address_url':fileaddress})
            
class StateDevView(ListAPIView):
    """ 根据cncstate字段查询不同状态的设备 """
    authentication_classes = [JwtAuth]
    serializer_class = StateDevSerializer
    pagination_class = MyPagination
        
    def list(self, request, *args, **kwargs):
        userinfo_id = self.request.user['id']
        cncstate= kwargs.get('cncstate')
        devnum= kwargs.get('devnum')
        if devnum =='all':
            if userinfo_id == 1 or userinfo_id == 19:
                if cncstate =='all':
                    queryset = Device.objects.all().order_by('id')
                else:
                    queryset = Device.objects.filter(cncstate=cncstate).all().order_by('id')
            else:
                if cncstate =='all':
                    queryset = Device.objects.filter(userinfo_id=userinfo_id).all().order_by('id')
                else: 
                    queryset = Device.objects.filter(userinfo_id=userinfo_id, cncstate=cncstate).all().order_by('id')
        else:
            queryset = Device.objects.filter(devnum=devnum).all().order_by('id')    
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

        



