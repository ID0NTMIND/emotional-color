from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from shared.db.database import engine
from shared.db.models import User
from typing import Generator, Optional

security = HTTPBearer(auto_error=False)  # не падаем, если заголовка нет


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = request.cookies.get('access_token')
    if not token and credentials:
        token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    user = db.exec(select(User).where(User.auth_token == token)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return user

# Функция для страниц: возвращает None, если пользователь не авторизован


def get_current_user_from_cookie(request: Request) -> Optional[User]:
    token = request.cookies.get('access_token')
    if not token:
        return None
    with Session(engine) as session:
        user = session.exec(select(User).where(
            User.auth_token == token)).first()
        return user
