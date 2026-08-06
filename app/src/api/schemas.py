from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserProfile(BaseModel):
    id: str
    username: str
    role: str
    balance: Decimal
    created_at: datetime


class BalanceTopUp(BaseModel):
    amount: Decimal = Field(..., gt=0)


class PredictionRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1024)


class PredictionResponse(BaseModel):
    task_id: str
    status: str
    label: Optional[str] = None
    confidence: Optional[Decimal] = None


class TransactionOut(BaseModel):
    id: str
    type: str
    amount: Decimal
    timestamp: datetime
    task_id: Optional[str] = None


class MLTaskOut(BaseModel):
    id: str
    model_name: str
    input_data: str
    status: str
    created_at: datetime
    label: Optional[str] = None
    confidence: Optional[Decimal] = None
