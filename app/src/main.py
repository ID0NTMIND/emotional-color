from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.init_db import init


@asynccontextmanager
async def lifespan(app: FastAPI):
    init()   # выполняется при запуске
    yield    # приложение работает

app = FastAPI(title="ML Service API", lifespan=lifespan)


@app.get("/")
async def root():
    return {"status": "ok"}
