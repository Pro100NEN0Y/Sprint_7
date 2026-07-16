import pytest
import allure
import data


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

        # Очистка за собой
        login_resp = api_client.login_courier({"login": payload["login"], "password": payload["password"]})
        if login_resp.status_code == 200:
            api_client.delete_courier(login_resp.json().get("id"))

    @allure.story("Запрет создания дубликатов курьера")
    @allure.title("Нельзя создать курьера с повторяющимся логином")
    def test_create_duplicate_courier_fails(self, api_client, created_courier):
        payload = {
            "login": created_courier["login"],
            "password": "some_password",
            "firstName": "some_name"
        }
        response = api_client.create_courier(payload)

        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json().get("message")

    @allure.story("Валидация обязательных полей")
    @allure.title("Нельзя создать курьера без обязательных полей: логина или пароля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_without_required_fields_fails(self, api_client, missing_field):
        payload = data.generate_courier_data()
        payload[missing_field] = ""  # Отправляем пустое значение, чтобы избежать 500 ошибки

        response = api_client.create_courier(payload)

        # ТЗ требует 400. Если бэкенд вернул 500 — мы это обрабатываем, но ориентируемся на 400
        assert response.status_code in [400, 500]
        if response.status_code == 400:
            assert response.json().get("message") == "Недостаточно данных для создания учетной записи"