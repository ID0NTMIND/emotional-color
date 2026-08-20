import requests
from tests.helpers import BALANCE


def test_get_initial_balance(user_headers):
    resp = requests.get(BALANCE, headers=user_headers)
    assert resp.status_code == 200
    assert resp.json()["balance"] == "0.00"


def test_topup_balance_success(user_headers):
    resp = requests.post(
        f"{BALANCE}/topup",
        json={"amount": 50}, headers=user_headers)
    assert resp.status_code == 200
    assert float(resp.json()["balance"]) == 50.0


def test_topup_balance_invalid_amount(user_headers):
    # Отрицательное число
    resp = requests.post(
        f"{BALANCE}/topup",
        json={"amount": -10}, headers=user_headers)
    assert resp.status_code == 422


def test_topup_balance_zero(user_headers):
    # Ноль тоже запрещён (gt=0)
    resp = requests.post(f"{BALANCE}/topup",
                         json={"amount": 0}, headers=user_headers)
    assert resp.status_code == 422


def test_balance_requires_auth():
    resp = requests.get(BALANCE)
    assert resp.status_code == 401
