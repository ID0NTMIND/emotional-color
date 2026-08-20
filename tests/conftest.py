import uuid
import pytest

from tests.helpers import register, login, auth_headers


@pytest.fixture
def new_user():
    """
    Создаёт нового пользователя, возвращает кортеж:
    (username, password, token)
    """
    username = f"test_{uuid.uuid4().hex[:6]}"
    password = "secret123"

    resp = register(username, password)
    assert resp.status_code == 200, f"Register failed: {resp.text}"
    token = resp.json()["access_token"]

    return username, password, token


@pytest.fixture
def user_headers(new_user):
    """Возвращает заголовки авторизации для созданного пользователя."""
    _, _, token = new_user
    return auth_headers(token)
