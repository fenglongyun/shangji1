#from shangji import settings
from rest_framework.authentication import BaseAuthentication
import jwt
from jwt import exceptions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.decorators import api_view

class JwtAuth(BaseAuthentication):
    
    def authenticate(self,request):
        token=request.META.get('HTTP_ACCESSTOKEN')
        salt='qwer123'
        try:
            payload=jwt.decode(token,salt,True)
        # except exceptions.ExpiredSignatureError:
        #     return False
        # except exceptions.DecodeError:
        #     return False
        # except exceptions.InvalidTokenError:
        #     return False
        except exceptions.ExpiredSignatureError:
            raise AuthenticationFailed({'code':0,'erro':'token已失效'})
        except exceptions.DecodeError:
            raise AuthenticationFailed({'code':0,'erro':'token认证失败'})
        except exceptions.InvalidTokenError:
            raise AuthenticationFailed({'code':0,'erro':'非法的token'})
        return (payload,token)

