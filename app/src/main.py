from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException, Request, Depends
from contextlib import asynccontextmanager
from src.db.init_db import init
from src.api import auth, users, balance, history, predictions
from fastapi.staticfiles import StaticFiles
from src.api.dependencies import get_current_user_from_cookie
from typing import Optional
from shared.db.models import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    init()
    yield

app = FastAPI(title="ML Service API", lifespan=lifespan)

templates = Jinja2Templates(directory="src/templates")

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(balance.router)
app.include_router(history.router)
app.include_router(predictions.router)


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request, current_user: Optional[User] = Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse(request, "index.html", {"current_user": current_user})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, current_user: Optional[User] = Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse(request, "login.html", {"current_user": current_user})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request, current_user: Optional[User] = Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse(request, "dashboard.html", {"current_user": current_user})


@app.get("/history", response_class=HTMLResponse)
async def history_page(request: Request, current_user: Optional[User] = Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse(request, "history.html", {"current_user": current_user})
