# main.py 【调整后完整顺序，重点：load_dotenv 放在所有导入前面】
from dotenv import load_dotenv
# 加载 .env 环境变量，必须在导入 agent / 读取环境变量的模块之前！
load_dotenv()

from fastapi import FastAPI
from fastapi import Depends
from routers.auth_router import router as auth_router
from routers.name_router import router as name_router


app = FastAPI(title="我的第一个FastAPI")

app.include_router(auth_router)
app.include_router(name_router)

@app.get("/")
async def root():
    return {"msg": "Hello FastAPI"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"hi {name}"}


