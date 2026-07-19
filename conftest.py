import pytest
import data
from api_client import ScooterApiClient

@pytest.fixture(scope="function")
def api_client():
    return ScooterApiClient()

@pytest.fixture(scope="function")
def created_courier(api_client):
    """Фикстура создает курьера перед тестом и гарантированно удаляет его после"""
    payload = data.generate_courier_data()
    api_client.create_courier(payload)
    
    yield payload  # Передаем данные курьера в тест
    
    # Автоматическая очистка после завершения теста
    login_resp = api_client.login_courier({"login": payload["login"], "password": payload["password"]})
    if login_resp.status_code == 200:
        courier_id = login_resp.json().get("id")
        api_client.delete_courier(courier_id)