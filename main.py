from fastapi import FastAPI
from routes.chat import router as chat_router
from routes.root import router as root_router

app = FastAPI()
app.include_router(root_router)
app.include_router(chat_router)
