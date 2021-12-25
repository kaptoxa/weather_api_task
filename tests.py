from requests import get

from config import API_URL

def test_empty():
    response = get(f'{API_URL}/')
    assert response.status_code == 200