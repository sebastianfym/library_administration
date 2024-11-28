import requests

from tests.config import TestConfig

test_config = TestConfig()

def test_user_api():
    data = {"username": "test_username", "password": "test_password"}
    response = requests.post(f"{test_config.server_full_path}user/register", json=data)
    assert response.status_code == 200

    response = requests.post(f"{test_config.server_full_path}user/login", json=data)
    assert response.status_code == 200

test_user_api()