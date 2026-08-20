from tests.helpers import register, login


def test_register_success(new_user):
    username, _, token = new_user
    assert token is not None

    # Повторная регистрация с тем же именем -> 400
    resp = register(username, "otherpass")
    assert resp.status_code == 400

# def test_register_missing_fields():
#     resp = register("", "")
#     import requests
#     from tests.helpers import AUTH_REGISTER
#     resp = requests.post(AUTH_REGISTER, json={})
#     assert resp.status_code == 422


def test_login_success(new_user):
    username, password, _ = new_user
    resp = login(username, password)
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password(new_user):
    username, _, _ = new_user
    resp = login(username, "wrongpassword")
    assert resp.status_code == 401


def test_login_wrong_username():
    resp = login("nonexistent_user", "any_pass")
    assert resp.status_code == 401
