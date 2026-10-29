from fastapi import APIRouter,HTTPException
from pydantic import EmailStr
from dependencies import get_session
from fastapi import Depends
from models import AsyncSession
import string
import random
from aiosmtplib import SMTPResponseException
from repository.user_repo import EmailCodeRepository,UserRepository
from schemas import ResponseOut
from schemas.user_schemas import RegisterIn,UserCreateSchema,LoginIn,LoginOut
from typing import Optional
from models.user import User
from core.auth import AuthHandler
from dependencies import Mailer,get_mailer

router = APIRouter(prefix="/auth",tags=["user"])

auth_handler = AuthHandler()

#获取邮箱验证码
@router.get("/code",response_model=ResponseOut)
async def get_email_code(
    email:EmailStr,
    mail:Mailer = Depends(get_mailer),
    session:AsyncSession = Depends(get_session)
):
    #1 生成4位验证码
    source = string.digits * 4
    code = "".join(random.sample(source,4))
    #2 发送验证码
    try:
        await mail.send(to_addr=email,subject='注册验证码',body=f"您的验证码为：{code},5分钟有效")
    except SMTPResponseException as e:
        raise HTTPException(500,detail="邮寄发送失败！")  

    email_code_repo = EmailCodeRepository(session=session)
    await email_code_repo.create(str(email),code)
    return ResponseOut()

# 注册用户
@router.post("/register",response_model=ResponseOut)
async def register(
    data:RegisterIn,
    session: AsyncSession = Depends(get_session)
):
    user_repo = UserRepository(session=session)
    #1 判断邮箱是否存在
    email_exist = await user_repo.email_is_exist(email=str(data.email))
    if email_exist:
        raise HTTPException(400,"该邮箱已经存在！")
    #2 校验验证码是否正确
    email_code_repo = EmailCodeRepository(session=session)
    email_code_match = await email_code_repo.check_email_code(email=str(data.email),code=data.code)
    if not email_code_match:
        raise HTTPException(400,"邮箱或者验证码错误！")
    try:
        await user_repo.create(UserCreateSchema(email=str(data.email),password=data.password,username=data.username))
    except Exception as e:
        raise HTTPException(500,detail=str(e))

    return ResponseOut

@router.post("/login",response_model=LoginOut)
async def login(
    data:LoginIn,
    session: AsyncSession = Depends(get_session)
    ):
    #1 创建user_repo 对象
    user_repo = UserRepository(session=session)
    #2 根据邮箱查找用户
    user : Optional[User]= await user_repo.get_by_email(str(data.email))
    if not user:
        raise HTTPException("400","该用户不存在")
    
    if not user.check_password(data.password):
        raise HTTPException("400","邮箱或密码错误")
    #3 生产jwt token
    tokens = auth_handler.encode_login_token(user.id)
    return {
        "user":user,
        "token":tokens['access_token']
    }
