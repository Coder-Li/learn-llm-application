from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.routing import RequestValidationError
from routes.chat import router as chat_router
from routes.root import router as root_router
from db.engine import engine
from db.models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时自动创建表
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

# region 全局异常处理
def error_payload(code: str, message: str):
    return {
        "error": {
            "code": code,
            "message": message
        }
    }

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=error_payload("invalid_request", "请求体格式或字段不正确")
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_payload("http_error", exc.detail)
    )

# endregion

app.include_router(root_router)
app.include_router(chat_router)
