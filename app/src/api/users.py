from fastapi import APIRouter, Depends
from src.api.dependencies import get_current_user
from src.api.schemas import UserProfile
from src.db.models import User
from decimal import Decimal

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserProfile)
def read_my_profile(current_user: User = Depends(get_current_user)) -> UserProfile:
    return UserProfile(
        id=str(current_user.id),
        username=current_user.username,
        role=current_user.role,
        balance=current_user.balance.amount if current_user.balance else Decimal(
            "0"),
        created_at=current_user.created_at,
    )
