from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.apis.deps import get_session
from app.apis.main import api_router
from app.web import web_router
from app.core.seed import run_initialization
from app.database.db import async_session_maker

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



@app.on_event("startup")
async def startup_event():
    async with async_session_maker() as session:
        await run_initialization(session)