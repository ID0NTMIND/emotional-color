from sqlmodel import Session, select
from .database import engine
from .models import User, Balance, MLModel, SQLModel
from decimal import Decimal


def init():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # 2. Проверяем, есть ли уже демо-пользователь
        if not session.exec(select(User).where(User.username == "demo")).first():
            # Демо-пользователь
            user = User(username="demo",
                        password_hash="demo_hash", role="user")
            session.add(user)
            session.flush()
            session.add(Balance(user_id=user.id, amount=Decimal("100.00")))

            # Демо-администратор (задание со звездочкой, пока не продумал все до конца с админом)
            admin = User(username="admin",
                         password_hash="admin_hash", role="admin")
            session.add(admin)
            session.flush()
            session.add(Balance(user_id=admin.id, amount=Decimal("1000.00")))

            # Базовая ML-модель
            model = MLModel(
                name="Text Sentiment Classifier",
                description="Модель для анализа тональности текста",
                cost_per_prediction=Decimal("1.00")
            )
            session.add(model)

            session.commit()
            print("Initial data created.")
        else:
            print("Initial data already exists.")
