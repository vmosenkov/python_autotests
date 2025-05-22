import requests
import pytest
import sys 
from pathlib import Path 

sys.path.append(str(Path(__file__).parent.parent))

from config import URL, API, TRAINER_TOKEN, TRAINER_ID, TRAINER_NAME  # Импортируем данные из config.py

BASE_URL = f"{URL}{API}"
HEADERS = {
    'Content-Type' : 'application/json',
    'trainer_token' : TRAINER_TOKEN
}

# Проверка статус кода 200
def test_status_code():
    response = requests.get(url = f'{BASE_URL}/trainers', params = {'trainer_id': TRAINER_ID})
    assert response.status_code == 200


# Провека имени
@pytest.mark.parametrize(
    'key, value',[
        ('trainer_name', TRAINER_NAME),
        ('id', TRAINER_ID),
    ]
)
def test_parametrize(key, value):
    response_parametrize = requests.get(url = f'{BASE_URL}/trainers', params = {'trainer_id': TRAINER_ID})
    assert response_parametrize.json()["data"][0][key] == value
