import jwt
import datetime
from django.conf import settings
def create_token(payload,timeout=1):
    salt='qwer123'
    payload['exp']=datetime.datetime.utcnow()+datetime.timedelta(days=timeout)
    token=jwt.encode(payload,salt,algorithm="HS256")
    return token
