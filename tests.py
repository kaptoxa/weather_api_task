from requests import get

from config import API_URL

example = "weather?country_code=RU&city=Moscow&date=<+/-5 дней>T12:00&cnt=5"

def test_empty():
    response = get(f'{API_URL}/')
    assert response.status_code == 200

def test_example():
    response = get(f'{API_URL}/{example}')
    assert response.status_code == 200
