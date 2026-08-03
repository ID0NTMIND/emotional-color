from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
import enum

# Перечисления статусов и типов транзакций


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class TransactionType(str, enum.Enum):
    DEBIT = "debit"
    CREDIT = "credit"


# Таблицы
class User(SQLModel, table=True):
    __tablename__: str = "users"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(unique=True, index=True)
    password_hash: str
    role: str = Field(default="user")
    created_at: datetime = Field(default_factory=datetime.now)

    # Связи
    balance: Optional["Balance"] = Relationship(back_populates="user")
    tasks: List["MLTask"] = Relationship(back_populates="user")


class Balance(SQLModel, table=True):
    __tablename__: str = 'balances'
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key='users.id', unique=True)
    amount: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    updated_at: datetime = Field(default_factory=datetime.now)

    user: "User" = Relationship(back_populates="balance")


class MLModel(SQLModel, table=True):
    __tablename__: str = 'ml_models'
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: Optional[str] = None
    cost_per_predictions: Decimal = Field(max_digits=10, decimal_places=2)

    tasks: List["MLTask"] = Relationship(back_populates="model")


class MLTask(SQLModel, table=True):
    __tablename__: str = "ml_tasks"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    model_id: UUID = Field(foreign_key="ml_models.id")
    input_data: str
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    user: "User" = Relationship(back_populates="tasks")
    model: "MLModel" = Relationship(back_populates="tasks")
    prediction: Optional["PredictionResult"] = Relationship(
        back_populates="task")


class PredictionResult(SQLModel, table=True):
    __tablename__: str = "prediction_results"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    task_id: UUID = Field(foreign_key="ml_tasks.id", unique=True)
    label: str
    confidence: Decimal = Field(max_digits=5, decimal_places=4)
    model_id: UUID = Field(foreign_key="ml_models.id")
    created_at: datetime = Field(default_factory=datetime.now)

    task: "MLTask" = Relationship(back_populates="prediction")


class Transaction(SQLModel, table=True):
    __tablename__: str = "transactions"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    amount: Decimal = Field(max_digits=10, decimal_places=2)
    type: TransactionType
    task_id: Optional[UUID] = Field(default=None, foreign_key="ml_tasks.id")
    timestamp: datetime = Field(default_factory=datetime.now)
