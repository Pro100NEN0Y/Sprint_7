import pytest
import allure
from api_client import ScooterApiClient
import data


@pytest.fixture(scope="function")
def api_client():
    return ScooterApiClient()


@pytest.fixture(scope="function")
def created_courier(api_client):
    """
    Фикстура создает уникального курьера перед тестом.
    После завершения теста удаляет курьера из базы данных.
    """
    courier_data = data.generate_courier_data()
    response = api_client.create_courier(courier_data)

    courier_id = None
    if response.status_code == 201:
        login_response = api_client.login_courier({
            "login": courier_data["login"],
            "password": courier_data["password"]
        })
        if login_response.status_code == 200:
            courier_id = login_response.json().get("id")

    yield {
        "login": courier_data["login"],
        "password": courier_data["password"],
        "firstName": courier_data["firstName"],
        "id": courier_id
    }

    if courier_id:
        with allure.step(f"Очистка: удаление курьера с id={courier_id}"):
            api_client.delete_courier(courier_id)