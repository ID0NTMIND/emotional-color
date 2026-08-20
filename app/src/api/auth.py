from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session
from src.api.dependencies import get_db
from shared.services.user_service import create_user, get_user_by_username
from src.core.security import get_password_hash, verify_password
from src.api.schemas import UserRegister, UserLogin, TokenResponse
import uuid

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(user_data: UserRegister, response: Response, db: Session = Depends(get_db)):
    if get_user_by_username(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed = get_password_hash(user_data.password)
    user = create_user(db, user_data.username, hashed, initial_balance=0)
    token = str(uuid.uuid4())
    user.auth_token = token
    db.add(user)
    db.commit()

    response.set_cookie(
        key="access_token",
        value=token,
        path="/",
        max_age=86400,   # 1 день
    )
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = get_user_by_username(db, user_data.username)
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = str(uuid.uuid4())
    user.auth_token = token
    db.add(user)
    db.commit()

    response.set_cookie(
        key="access_token",
        value=token,
        path="/",
        max_age=86400,
    )
    return TokenResponse(access_token=token)
