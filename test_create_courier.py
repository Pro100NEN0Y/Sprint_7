import pytest
import allure
import data
import text_messages

@allure.epic("Яндекс Самокат API")
@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.story("Успешное создание курьера")
    @allure.title("Курьера можно успешно создать с валидными данными")
    def test_success_create_courier(self, api_client):
        payload = data.generate_courier_data()
        response = api_client.create_courier(payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        # Локальная очистка для этого конкретного теста
        login_resp = api_client.login_courier({"login": payload["login"], "password": payload["password"]})
        if login_resp.status_code == 200:
            api_client.delete_courier(login_resp.json().get("id"))

    @allure.story("Запрет создания дубликатов")
    @allure.title("Нельзя создать курьера с повторяющимся логином")
    def test_create_duplicate_courier_fails(self, api_client, created_courier):
        payload = {
            "login": created_courier["login"],
            "password": "password123",
            "firstName": "test_name"
        }
        response = api_client.create_courier(payload)

        assert response.status_code == 409
        assert text_messages.DUPLICATE_LOGIN_ERROR in response.json().get("message")

    @allure.story("Валидация обязательных полей")
    @allure.title("Нельзя создать курьера без логина или пароля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_without_required_fields_fails(self, api_client, missing_field):
        payload = data.generate_courier_data()
        payload[missing_field] = ""  # Передаем пустое поле вместо удаления ключа

        response = api_client.create_courier(payload)

        assert response.status_code == 400
        assert response.json().get("message") == text_messages.MISSING_FIELDS_CREATE_ERROR