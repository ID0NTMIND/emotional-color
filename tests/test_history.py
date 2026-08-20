# tests/test_history.py
import time
import requests

from tests.helpers import BALANCE, PREDICT, HISTORY_TRANSACTIONS, HISTORY_PREDICTIONS


def test_history_transactions_after_operations(user_headers):
    # Пополнение и предсказание
    requests.post(f"{BALANCE}/topup", json={"amount": 5}, headers=user_headers)
    requests.post(PREDICT, json={"text": "Nice"}, headers=user_headers)
    time.sleep(2)

    resp = requests.get(HISTORY_TRANSACTIONS, headers=user_headers)
    assert resp.status_code == 200
    transactions = resp.json()
    assert len(transactions) >= 2


def test_history_predictions_after_prediction(user_headers):
    requests.post(f"{BALANCE}/topup", json={"amount": 5}, headers=user_headers)
    requests.post(PREDICT, json={"text": "Great"}, headers=user_headers)
    time.sleep(2)

    resp = requests.get(HISTORY_PREDICTIONS, headers=user_headers)
    assert resp.status_code == 200
    predictions = resp.json()
    assert len(predictions) >= 1


def test_history_requires_auth():
    resp = requests.get(HISTORY_TRANSACTIONS)
    assert resp.status_code == 401
