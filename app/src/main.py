from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.init_db import init
from src.api import auth, users, balance, history, predictions


@asynccontextmanager
async def lifespan(app: FastAPI):
    init()
    yield

app = FastAPI(title="ML Service API", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(balance.router)
app.include_router(history.router)
app.include_router(predictions.router)


@app.get("/")
async def root():
    return {"status": "ok"}
