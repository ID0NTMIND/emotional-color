from fastapi import APIRouter, Depends
from sqlmodel import Session
from src.api.dependencies import get_current_user, get_db
from src.services.user_service import get_user_history
from src.api.schemas import TransactionOut, MLTaskOut
from src.db.models import User
from typing import List

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/transactions", response_model=List[TransactionOut])
def get_transactions(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[TransactionOut]:
    transactions, _ = get_user_history(db, current_user, limit=limit)
    return [
        TransactionOut(
            id=str(t.id),
            type=t.transaction_type.value,
            amount=t.amount,
            timestamp=t.timestamp,
            task_id=str(t.task_id) if t.task_id else None,
        )
        for t in transactions
    ]


@router.get("/predictions", response_model=List[MLTaskOut])
def get_predictions(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[MLTaskOut]:
    _, tasks = get_user_history(db, current_user, limit=limit)
    return [
        MLTaskOut(
            id=str(task.id),
            model_name=task.model.name if task.model else "unknown",
            input_data=task.input_data,
            status=task.status,
            created_at=task.created_at,
            label=task.prediction.label if task.prediction else None,
            confidence=task.prediction.confidence if task.prediction else None,
        )
        for task in tasks
    ]
