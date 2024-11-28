import requests

from tests.config import TestConfig

test_config = TestConfig()

def test_author_api():
    data = {"first_name": "test_first_name", "second_name": "test_second_name"}
    response = requests.post(f"{test_config.server_full_path}author/", json=data)
    assert response.status_code == 200


test_author_api()