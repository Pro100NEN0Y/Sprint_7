import requests
import allure
import data


class ScooterApiClient:

    @allure.step("Создание курьера с данными: {payload}")
    def create_courier(self, payload):
        return requests.post(data.CREATE_COURIER_URL, json=payload)

    @allure.step("Авторизация курьера с данными: {payload}")
    def login_courier(self, payload):
        return requests.post(data.LOGIN_COURIER_URL, json=payload)

    @allure.step("Удаление курьера по id: {courier_id}")
    def delete_courier(self, courier_id):
        return requests.delete(f"{data.DELETE_COURIER_URL}{courier_id}")

    @allure.step("Создание заказа с телом: {payload}")
    def create_order(self, payload):
        return requests.post(data.ORDERS_URL, json=payload)

    @allure.step("Получение списка заказов")
    def get_orders_list(self, params=None):
        return requests.get(data.ORDERS_URL, params=params)