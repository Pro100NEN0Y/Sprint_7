import pytest
import allure
import text_messages

@allure.epic("Яндекс Самокат API")
@allure.feature("Авторизация курьера")
class TestLoginCourier:

    @allure.story("Успешная авторизация")
    @allure.title("Курьер может успешно авторизоваться с верными данными")
    def test_success_login_courier(self, api_client, created_courier):
        payload = {
            "login": created_courier["login"],
            "password": created_courier["password"]
        }
        response = api_client.login_courier(payload)

        assert response.status_code == 200
        assert isinstance(response.json().get("id"), int)

    @allure.story("Валидация полей авторизации")
    @allure.title("При отсутствии логина или пароля возвращается ошибка 400")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_without_required_fields_fails(self, api_client, created_courier, missing_field):
        payload = {
            "login": created_courier["login"],
            "password": created_courier["password"]
        }
        payload[missing_field] = ""

        response = api_client.login_courier(payload)

        assert response.status_code == 400
        assert response.json().get("message") == text_messages.MISSING_FIELDS_LOGIN_ERROR

    @allure.story("Некорректный пароль")
    @allure.title("Система возвращает 404 при неверном пароле существующего курьера")
    def test_login_with_incorrect_password_fails(self, api_client, created_courier):
        payload = {
            "login": created_courier["login"],
            "password": "absolutely_wrong_password"
        }
        response = api_client.login_courier(payload)

        assert response.status_code == 404
        assert text_messages.ACCOUNT_NOT_FOUND_ERROR in response.json().get("message")

    @allure.story("Несуществующий пользователь")
    @allure.title("Система возвращает 404 при попытке авторизации несуществующего логина")
    def test_login_non_existent_user_fails(self, api_client):
        payload = {
            "login": "non_existent_courier_login_9999",
            "password": "some_password"
        }
        response = api_client.login_courier(payload)

        assert response.status_code == 404
        assert text_messages.ACCOUNT_NOT_FOUND_ERROR in response.json().get("message")