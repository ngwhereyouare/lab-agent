import asyncio
from contextlib import asynccontextmanager
import traceback

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from app.config import UPLOAD_DIR
from app.models.user import User
from app.models.lab import Lab
from app.models.equipment import Equipment
from app.models.reservation import Reservation
from app.database import Base, engine
from app.api import api
from fastapi.exceptions import RequestValidationError
from app.common.exceptions import (
    BusinessException,
    bussiness_excpetion_hadler,
    http_excpetion_hadler,
    validation_excpetion_hadler,
    global_excpetion_hadler,
)
from starlette.middleware.cors import CORSMiddleware

from app.services import kb_service, reservation_service

Base.metadata.create_all(bind=engine)  # 自动帮我们创建数据库和表结构


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 预热向量库：模型加载（约 15s）挪到启动阶段，避免首个请求超过前端 30s 超时
    try:
        await asyncio.to_thread(kb_service.warmup)  # to_thread：别阻塞事件循环
    except Exception:
        traceback.print_exc()
    # 启动项目开启异步的扫描任务
    task = asyncio.create_task(reservation_service.run_expire_scan())
    yield
    task.cancel()  # 关闭项目同时取消异步任务
    await asyncio.gather(
        task, return_exceptions=True
    )  # 取消任务不再把CancelError抛给lifespan


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的前端源，不要直接写 ["*"]
    allow_credentials=True,  # ✅ 关键：允许前端携带 Authorization token
    allow_methods=["*"],  # 允许所有请求方法 GET POST PUT DELETE OPTIONS
    allow_headers=["*"],  # 允许所有请求头（包含Authorization）
)

app.include_router(api)


# 注册异常处理器
app.add_exception_handler(BusinessException, bussiness_excpetion_hadler)
app.add_exception_handler(HTTPException, http_excpetion_hadler)
app.add_exception_handler(RequestValidationError, validation_excpetion_hadler)
# 全局的异常兜底，必须放在最后注册！！
app.add_exception_handler(Exception, global_excpetion_hadler)

# 挂载静态的文件目录

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}
