from pydantic import BaseModel,Field,EmailStr,model_validator
from typing import Annotated,Literal,List
from  models.user import User

userNameStr = Annotated[str,Field(...,min_length=4,max_length=20,description="用户名")]

rawPasswordStr = Annotated[str,Field(...,min_length=6,max_length=20,description="密码")]


class RegisterIn(BaseModel):
    email:EmailStr
    username:userNameStr
    password:rawPasswordStr
    confirm_password:rawPasswordStr
    code:Annotated[str,Field(...,min_length=4,max_length=4)]

    @model_validator(mode="after")
    def password_is_match(self)->"RegisterIn":
        password = self.password
        confirm_password = self.confirm_password
        if password!=confirm_password :
            raise ValueError("密码不一致")
        return self

class UserCreateSchema(BaseModel):
    email: EmailStr
    password:rawPasswordStr
    username:userNameStr

class LoginIn(BaseModel):
    email:EmailStr
    password:rawPasswordStr

class UserSchema(BaseModel):
    id:Annotated[int,Field(...)]
    email: EmailStr
    username:userNameStr

class LoginOut(BaseModel):
    user:UserSchema
    token:str


