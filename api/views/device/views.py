from  rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Device
from api.auth import JwtAuth
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
            return Response({'code':'1', 'msg':'上传成功'})
            
