import requests
import allure
import urls

class ScooterApiClient:

    @allure.step("Создание курьера с данными: {payload}")
    def create_courier(self, payload):
        return requests.post(urls.CREATE_COURIER_URL, json=payload)

    @allure.step("Авторизация курьера с данными: {payload}")
    def login_courier(self, payload):
        return requests.post(urls.LOGIN_COURIER_URL, json=payload)

    @allure.step("Удаление курьера по id: {courier_id}")
    def delete_courier(self, courier_id):
        return requests.delete(f"{urls.DELETE_COURIER_URL}{courier_id}")