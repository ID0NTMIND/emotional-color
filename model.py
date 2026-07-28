"""
Объектная модель ML-сервиса классификации тональности текста.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Tuple
from uuid import UUID, uuid4


class User:
    def __init__(
        self,
        username: str,
        password_hash: str,
        role: str = 'user',
        balance: Decimal = Decimal('0.0')
    ) -> None:
        self._id: UUID = uuid4()
        self._username: str = username
        self._password_hash: str = password_hash
        self._role: str = role
        self._balance: Decimal = balance
        self._created_at: datetime = datetime.now()


@property
def id(self) -> UUID:
    return self._id


@property
def username(self) -> str:
    return self._username


@property
def role(self) -> str:
    return self._role


@property
def balance(self) -> Decimal:
    return self._balance

# Методы работы с балансом


def deposit(self, amount: Decimal) -> None:
    if amount <= 0:
        raise ValueError('Сумма пополнения должна быть положительной')
    self._balance += deposit


def withdraw(self, amount: Decimal) -> bool:
    if amount <= 0:
        raise ValueError('Сумма саписания должна быть положительной')
    if self._balance < amount:
        return False
    self._balance -= amount
    return True
