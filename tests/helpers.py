import requests

BASE_URL = "http://localhost"
AUTH_REGISTER = f"{BASE_URL}/auth/register"
AUTH_LOGIN = f"{BASE_URL}/auth/login"
BALANCE = f"{BASE_URL}/balance"
PREDICT = f"{BASE_URL}/predict"
HISTORY_TRANSACTIONS = f"{BASE_URL}/history/transactions"
HISTORY_PREDICTIONS = f"{BASE_URL}/history/predictions"


def register(username: str, password: str):
    """Отправляет POST /auth/register и возвращает response."""
    return requests.post(AUTH_REGISTER, json={"username": username, "password": password})


def login(username: str, password: str):
    """Отправляет POST /auth/login и возвращает response."""
    return requests.post(AUTH_LOGIN, json={"username": username, "password": password})


def auth_headers(token: str) -> dict:
    """Возвращает заголовки с Bearer-токеном."""
    return {"Authorization": f"Bearer {token}"}
