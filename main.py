from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.apis.main import api_router
from app.web import web_router

app = FastAPI(
    title="SnovaTour Travel Guides API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # для разработки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем шаблоны


# Подключаем статику (css/js)
app.mount("/static", StaticFiles(directory="app/web/static"), name="static")

app.include_router(api_router, prefix="/api")
app.include_router(web_router, tags=["Web Routes"])
