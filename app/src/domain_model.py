"""
Объектная модель ML-сервиса классификации тональности текста.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Tuple
from uuid import UUID, uuid4


class Balance:
    def __init__(
        self,
        user_id: UUID,
        amount: Decimal = Decimal('0.0'),
    ) -> None:
        if amount < 0:
            raise ValueError("Начальный баланс не может быть отрицательным")
        self._id: UUID = uuid4()
        self._user_id: UUID = user_id
        self._amount: Decimal = amount
        self._updated_at: datetime = datetime.now()

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def amount(self):
        return self._amount

    # Методы работы с балансом

    def deposit(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self._amount += amount
        self._updated_at = datetime.now()

    def withdraw(self, amount: Decimal) -> bool:
        if amount <= 0:
            raise ValueError("Сумма списания должна быть положительной")
        if self._amount < amount:
            return False
        self._amount -= amount
        self._updated_at = datetime.now()
        return True


class User:
    def __init__(
        self,
        username: str,
        password_hash: str,
        role: str = 'user'
    ) -> None:
        self._id: UUID = uuid4()
        self._username: str = username
        self._password_hash: str = password_hash
        self._role: str = role
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

    def is_admin(self) -> bool:
        return self._role == "admin"


class MLModel(ABC):
    """Абстрактный класс для ML моделей"""

    def __init__(
        self,
        name: str,
        description: str,
        cost_per_prediction: Decimal,
    ) -> None:
        self._id: UUID = uuid4()
        self._name: str = name
        self._description: str = description
        self._cost: Decimal = cost_per_prediction

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def cost_per_prediction(self) -> Decimal:
        return self._cost

    @abstractmethod
    def predict(self, input_data: str) -> "PredictionResult":
        """
        Выполнить предсказание на одном экземпляре данных.
        Реализация должна возвращать объект PredictionResult.
        """
        ...

    @abstractmethod
    def validate(self, input_data: str) -> Tuple[bool, List[str]]:
        """
        Валидирует входные данные.
        Возвращает (True, []) если данные корректны,
        (False, список ошибок) если есть ошибки.
        """
        ...


class TextSentimentModel(MLModel):
    """
    Модель классификации окраски текста на базе HuggingFace.
    Предварительно использует lxyuan/distilbert-base-multilingual-cased-sentiments-student (возможно изменю позже)
    """

    def __init__(self, cost: Decimal = Decimal('1.0'), max_text_length: int = 512) -> None:
        super().__init__(
            name="Text Sentiment Classifier",
            description="Модель классификации текста на классы: positive, neutral, negative",
            cost_per_prediction=cost
        )

        self._pipeline = None  # Заглушка под модель которую выберу
        self._max_text_length = max_text_length

    def predict(self, input_data: str) -> "PredictionResult":
        """Запускает пайплайн и возвращает PredictionResult."""
        # Здесь будет вызов self._pipeline(input_data)
        # Заглушка
        return PredictionResult(
            label="neutral",
            confidence=Decimal("0.95"),
            model_id=self._id,
        )

    def validate(self, input_data: str) -> Tuple[bool, List[str]]:
        """Проверяет что текст не пустой, и не превышает максимальную длину"""
        errors = []
        if not input_data or not input_data.strip():
            errors.append("Текст не может быть пустым")
        if len(input_data) > self._max_text_length:
            errors.append(
                f"Максимальная длина текста - {self._max_text_length} символов")
        return len(errors) == 0, errors


class PredictionResult:
    """Результат одного предсказания модели"""

    def __init__(
        self,
        label: str,
        confidence: Decimal,
        model_id: UUID
    ) -> None:
        self._id: UUID = uuid4()
        self._label: str = label
        self._confidence: Decimal = confidence
        self._model_id: UUID = model_id
        self._created_at: datetime = datetime.now()

    @property
    def label(self) -> str:
        return self._label

    @property
    def confidence(self) -> Decimal:
        return self._confidence

    @property
    def model_id(self) -> UUID:
        return self._model_id


class MLTask:
    """Задача поставленная пользователем для ML-модели."""

    STATUS_PENDING = "pending"
    STATUS_PROCESSING = "processing"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"

    def __init__(
        self,
        user: User,
        model: MLModel,
        input_data: str
    ) -> None:
        self._id: UUID = uuid4()
        self._user_id: UUID = user.id
        self._model_id: UUID = model.id
        self._input_data: str = input_data
        self._status = self.STATUS_PENDING
        self._result: Optional[PredictionResult] = None
        self._created_at: datetime = datetime.now()
        self._updated_at: datetime = self._created_at

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def model_id(self) -> UUID:
        return self._model_id

    @property
    def status(self) -> str:
        return self._status

    @property
    def result(self) -> Optional[PredictionResult]:
        return self._result

    def start_processing(self) -> None:
        """Переводит задачу в статус обработки."""
        self._status = self.STATUS_PROCESSING
        self._updated_at = datetime.now()

    def complete(self, result: PredictionResult) -> None:
        """Фиксирует успешное завершение задачи."""
        self._result = result
        self._status = self.STATUS_COMPLETED
        self._updated_at = datetime.now()

    def fail(self) -> None:
        """Помечает задачу как проваленную."""
        self._status = self.STATUS_FAILED
        self._updated_at = datetime.now()


class Transaction(ABC):
    """Абстрактная транзакция"""

    def __init__(
        self,
        user: User,
        amount: Decimal,
        task: Optional[MLTask] = None
    ) -> None:
        self._id: UUID = uuid4()
        self._user_id: UUID = user.id
        self._amount: Decimal = amount
        self._task_id: Optional[UUID] = task.id if task else None
        self._timestamp: datetime = datetime.now()

    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def task_id(self) -> Optional[UUID]:
        return self._task_id

    @abstractmethod
    def apply(self, balance: Balance) -> None:
        """Применить транзакцию к балансу. Полиморфный метод."""
        ...


class DebitTransaction(Transaction):
    """Списание средств за использование модели"""

    def apply(self, balance: Balance) -> None:
        success = balance.withdraw(self._amount)
        if not success:
            raise ValueError("Недостаточно средств на балансе")


class CreditTransaction(Transaction):
    """Пополнение баланса (позже возможно администратором тоже, пока хз)"""

    def apply(self, balance: Balance) -> None:
        balance.deposit(self._amount)


if __name__ == "__main__":
    # Создаём пользователей
    user = User(username="demo", password_hash="hash")
    admin = User(username="admin", password_hash="adminhash", role="admin")

    # Создаём балансы для пользователей (в реальности баланс будет создаваться при регистрации? (идея))
    user_balance = Balance(user_id=user.id, amount=Decimal("10"))
    admin_balance = Balance(user_id=admin.id, amount=Decimal("100"))

    print(f"User balance: {user_balance.amount}")
    print(f"Admin balance: {admin_balance.amount}")

    # Администратор пополняет баланс пользователю
    # (получает объект Balance пользователя по user_id — в реальном приложении через репозиторий)
    if admin.is_admin():
        user_balance.deposit(Decimal("50"))
        print(f"Admin topped up user. New user balance: {user_balance.amount}")

    # Выполнение ML-задачи
    model = TextSentimentModel()
    task = MLTask(user, model, "Отличный сервис!")
    task.start_processing()
    result = model.predict(task._input_data)
    task.complete(result)

    # Списание средств через транзакцию
    debit = DebitTransaction(user, model.cost_per_prediction, task)
    debit.apply(user_balance)
    print(f"User balance after debit: {user_balance.amount}")

    # Проверка результата
    if task.result is not None:
        print(
            f"Task result: {task.result.label}, confidence: {task.result.confidence}")
