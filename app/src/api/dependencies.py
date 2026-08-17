from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from shared.db.database import engine
from shared.db.models import User
from typing import Generator, Optional

security = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    user = db.exec(select(User).where(User.auth_token == token)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return user


def get_current_user_from_cookie(request: Request) -> Optional[User]:
    token = request.cookies.get('access_token')
    if not token:
        return None
    with Session(engine) as session:
        user = session.exec(select(User).where(
            User.auth_token == token)).first()
        return user
