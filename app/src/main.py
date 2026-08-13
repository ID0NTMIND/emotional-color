from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from src.db.init_db import init
from src.api import auth, users, balance, history, predictions
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    init()
    yield

app = FastAPI(title="ML Service API", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(balance.router)
app.include_router(history.router)
app.include_router(predictions.router)


@app.get("/{page}.html")
async def read_page(page: str):
    # Проверяем, что файл существует, иначе отдаём 404
    allowed = {"index", "login", "dashboard", "history"}
    if page not in allowed:
        raise HTTPException(status_code=404, detail="Page not found")
    return FileResponse(f"src/static/{page}.html")
