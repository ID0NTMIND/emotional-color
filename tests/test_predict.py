
import time
import requests

from tests.helpers import BALANCE, PREDICT, HISTORY_PREDICTIONS


def test_predict_success_and_deduction(user_headers):
    # Пополним баланс
    requests.post(
        f"{BALANCE}/topup",
        json={"amount": 10},
        headers=user_headers
    )

    before = float(requests.get(
        BALANCE, headers=user_headers).json()["balance"])

    resp = requests.post(
        PREDICT, json={"text": "I love this service"}, headers=user_headers)
    assert resp.status_code == 200
    task_id = resp.json()["task_id"]

    # Даём воркеру время обработать
    time.sleep(4)

    after = float(requests.get(
        BALANCE, headers=user_headers).json()["balance"])
    assert after == before - 1.0

    # Проверяем, что задача завершилась
    pred_hist = requests.get(HISTORY_PREDICTIONS, headers=user_headers)
    assert pred_hist.status_code == 200
    predictions = pred_hist.json()
    assert any(p["id"] == task_id and p["status"]
               == "completed" for p in predictions)


def test_predict_insufficient_balance(user_headers):
    # Баланс 0, не пополняем
    resp = requests.post(PREDICT, json={"text": "test"}, headers=user_headers)
    assert resp.status_code == 402


def test_predict_invalid_text(user_headers):
    resp = requests.post(PREDICT, json={"text": ""}, headers=user_headers)
    assert resp.status_code == 422


def test_predict_requires_auth():
    resp = requests.post(PREDICT, json={"text": "hello"})
    assert resp.status_code == 401
