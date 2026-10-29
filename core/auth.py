import jwt
from fastapi import HTTPException,Security,status
from enum import Enum
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import settings
from datetime import datetime



from threading import Lock

class SingletonMeta(type):
    """
    this is a thread-safe implementation of singleton
    """
    _instances = {}
    _lock : Lock= Lock()

    def __call__(cls, *args, **kwds):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwds)
                cls._instances[cls] = instance 


        return cls._instances[cls]


class TokenTypeEnum(Enum):
    ACCESS_TOKEN=1
    REFRESH_TOKEN=2

class AuthHandler(metaclass = SingletonMeta):
    security = HTTPBearer()

    secret = settings.JWT_SECRET_KEY

    def _encode_token(self,user_id:int,type:TokenTypeEnum):
        payload = dict(
            iss = user_id,
            sub = int(type.value)
        )

        to_encode = payload.copy()
        if type == TokenTypeEnum.ACCESS_TOKEN:
            exp = datetime.now() + settings.JWT_ACCESS_TOKEN_EXPIRES
        else:
            exp = datetime.now() + settings.JWT_REFRESH_TOKEN_EXPIRES

        to_encode.update({"exp":int(exp.timestamp())})
        return jwt.encode(to_encode,self.secret,algorithm='HS256')

    def encode_login_token(self,user_id:int):
        access_token = self._encode_token(user_id,TokenTypeEnum.ACCESS_TOKEN)
        refresh_token = self._encode_token(user_id,TokenTypeEnum.REFRESH_TOKEN)
        login_token = dict(
            access_token = f"{access_token}",
            refresh_token = f"{refresh_token}"
        )
        return login_token

    def encode_update_token(self,user_id):
        access_token = self._encode_token(user_id,TokenTypeEnum.ACCESS_TOKEN)
        update_token = dict(
            access_token = f"{access_token}"
        )
        return update_token

    def decode_access_token(self,token):
        try:
            payload = jwt.decode(token,self.secret,algorithms="HS256")
            if payload['sub'] != int(TokenTypeEnum.ACCESS_TOKEN.value):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Token类型错误!")
            return payload['iss']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Access Token 已过期！")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Access Token 不可用！")

    def decode_refresh_token(self,token):
        try:
            payload = jwt.decode(token,self.secret,algorithms="HS256")
            if payload['sub'] != int(TokenTypeEnum.REFRESH_TOKEN.value):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token类型错误!")
            return payload['iss']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Refresh Token 已过期！")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Refresh Token 不可用！")

    def auth_access_dependency(self,auth:HTTPAuthorizationCredentials = Security(security)):
        return self.decode_access_token(auth.credentials)

    def auth_refresh_dependency(self,auth:HTTPAuthorizationCredentials = Security(security)):
        return self.decode_refresh_token(auth.credentials)