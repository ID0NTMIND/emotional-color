from sqlmodel import Session, select, col, desc
from src.db.models import User, Balance, Transaction, MLTask, TransactionType
from decimal import Decimal
from typing import List, Tuple, Optional


def create_user(session: Session, username: str, password_hash: str, role: str = "user", initial_balance: Decimal = Decimal("0")) -> User:
    """Создаёт пользователя и его баланс"""
    user = User(username=username, password_hash=password_hash, role=role)
    session.add(user)
    session.flush()
    balance = Balance(user_id=user.id, amount=initial_balance)
    session.add(balance)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_username(session: Session, username: str) -> Optional[User]:
    """Находит пользователя по имени"""
    return session.exec(select(User).where(User.username == username)).first()


def top_up_balance(session: Session, user: User, amount: Decimal) -> Balance:
    """Пополняет баланс и записывает транзакцию."""
    if amount <= 0:
        raise ValueError("Сумма должна быть положительной")
    if user.balance is None:
        raise RuntimeError(
            f"У пользователя {user.username} отсутствует баланс")
    user.balance.amount += amount
    transaction = Transaction(
        user_id=user.id, amount=amount, transaction_type=TransactionType.CREDIT)
    session.add(transaction)
    session.commit()
    session.refresh(user.balance)
    return user.balance


def deduct_balance(session: Session, user: User, amount: Decimal, task: Optional[MLTask] = None) -> bool:
    """Списывает средства, если хватает. Возвращает True, если успешно."""
    if amount <= 0:
        raise ValueError("Сумма должна быть положительной")
    if user.balance is None:
        raise RuntimeError(
            f"У пользователя {user.username} отсутствует баланс")
    if user.balance.amount < amount:
        return False
    user.balance.amount -= amount
    transaction = Transaction(user_id=user.id, amount=amount,
                              transaction_type=TransactionType.DEBIT, task_id=task.id if task else None)
    session.add(transaction)
    session.commit()
    return True


def get_user_history(session: Session, user: User, limit: int = 10) -> Tuple[List[Transaction], List[MLTask]]:
    transactions = list(
        session.exec(
            select(Transaction)
            .where(Transaction.user_id == user.id)
            .order_by(desc(col(Transaction.timestamp)))
            .limit(limit)
        ).all()
    )
    tasks = list(
        session.exec(
            select(MLTask)
            .where(MLTask.user_id == user.id)
            .order_by(desc(col(MLTask.created_at)))
            .limit(limit)
        ).all()
    )
    return transactions, tasks
