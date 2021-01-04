from rest_framework.views import APIView
from rest_framework.response import Response
import hashlib
import requests
import json

# sim卡接口
class Simcard(APIView):
    def get(self,request,*args, **kwagrs):
        sid ='11951'
        apikey='13286307b450491f83af2bd3a4f53fce'
        msisdns='1440461308606'
        ts='20201125151900'

        data=sid+apikey+ts+msisdns
        newmd5=hashlib.md5()
        newmd5.update(data.encode(encoding='utf-8'))
        sign=newmd5.hexdigest()
        url='http://106.14.19.179:9011/iotapi/rest/v2/card/usage/current?sid='+ sid +'&sign='+ sign +'&ts='+ts+'&msisdns='+ msisdns
        # url1='http://106.14.19.179:9011/iotapi/rest/v2/card/pkg/get?sid='+ sid +'&sign='+ sign +'&ts='+ts+'&msisdn='+ msisdns
        res=requests.get(url)
        # res1=requests.get(url1)
        data=json.loads(res.text)
        return Response(data)



