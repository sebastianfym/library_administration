import requests

from tests.config import TestConfig

test_config = TestConfig()

def test_book_api():
    data = {
        "year":1026,
        "title":"Test book",
        "status":"ISSUED",
        "author_id":1
    }
    headers = {"Authorization": "Bearer token"}
    response = requests.post(f"{test_config.server_full_path}book/", json=data, headers=headers)
    test_book_id = response.json()['detail']['id']
    assert response.status_code == 200

    response = requests.get(f"{test_config.server_full_path}book/{test_book_id}", headers=headers)
    assert response.status_code == 200

    data = {"status": "issued"}
    response = requests.patch(f"{test_config.server_full_path}book/{test_book_id}", json=data, headers=headers)
    assert response.status_code == 200

    response = requests.delete(f"{test_config.server_full_path}book/{test_book_id}", headers=headers)
    assert response.status_code == 200




test_book_api()