from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from src.api.dependencies import get_current_user, get_db
from src.api.schemas import PredictionRequest, PredictionResponse
from src.db.models import MLModel, MLTask, PredictionResult, User
from src.services.user_service import deduct_balance
from decimal import Decimal
from src.db.models import TaskStatus

router = APIRouter(prefix="/predict", tags=["predictions"])


@router.post("", response_model=PredictionResponse)
def create_prediction(
    request: PredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> PredictionResponse:
    model = db.exec(select(MLModel).where(
        MLModel.name == "Text Sentiment Classifier")).first()
    if not model:
        raise HTTPException(status_code=500, detail="No ML model available")

    cost = model.cost_per_prediction
    if current_user.balance is None or current_user.balance.amount < cost:
        raise HTTPException(status_code=402, detail="Insufficient balance")

    task = MLTask(
        user_id=current_user.id,
        model_id=model.id,
        input_data=request.text,
        status=TaskStatus.PENDING,
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    success = deduct_balance(db, current_user, cost, task)
    if not success:
        db.delete(task)
        db.commit()
        raise HTTPException(status_code=500, detail="Balance deduction failed")

    # Заглушка результата
    label = "neutral"
    confidence = Decimal("0.9")
    prediction = PredictionResult(
        task_id=task.id,
        label=label,
        confidence=confidence,
        model_id=model.id,
    )
    db.add(prediction)
    task.status = TaskStatus.COMPLETED
    db.add(task)
    db.commit()

    return PredictionResponse(
        task_id=str(task.id),
        status=task.status,
        label=label,
        confidence=confidence,
    )
