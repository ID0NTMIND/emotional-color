from sqlmodel import create_engine, Session
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://user:pass@localhost:5432/mldb")

engine = create_engine(DATABASE_URL)


def get_session():
    '''Создаем сессию для работы с БД '''
    with Session(engine) as session:
        yield session
