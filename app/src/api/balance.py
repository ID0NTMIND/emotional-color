from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from src.api.dependencies import get_current_user, get_db
from src.services.user_service import top_up_balance
from src.api.schemas import BalanceTopUp
from src.db.models import User


router = APIRouter(prefix="/balance", tags=["balance"])


@router.get("")
def get_balance(current_user: User = Depends(get_current_user)) -> dict:
    if current_user.balance is None:
        raise HTTPException(status_code=400, detail="No balance record")
    return {"balance": str(current_user.balance)}


@router.post("/topup")
def topup_balance(
    data: BalanceTopUp,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    if current_user.balance is None:
        raise HTTPException(status_code=400, detail="No balance record")
    updated = top_up_balance(db, current_user, data.amount)
    return {"balance": str(updated.amount)}
