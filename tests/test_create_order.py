import pytest
import allure


@allure.epic("Яндекс Самокат API")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.story("Параметризованное создание заказа с разным выбором цвета")
    @allure.title("Заказ успешно создается с цветом: {color_value}")
    @pytest.mark.parametrize("color_value", [
        ["BLACK"],          # Только черный
        ["GREY"],           # Только серый
        ["BLACK", "GREY"],  # Оба цвета
        []                  # Без цвета
    ])
    def test_create_order_with_different_colors(self, api_client, color_value):
        order_payload = {
            "firstName": "Иван",
            "lastName": "Иванов",
            "address": "ул. Пушкина, д. 10, кв. 5",
            "metroStation": 4,
            "phone": "+7 999 123 45 67",
            "rentTime": 3,
            "deliveryDate": "2026-08-01",
            "comment": "Жду у подъезда",
            "color": color_value
        }

        response = api_client.create_order(order_payload)

        assert response.status_code == 201
        assert "track" in response.json()  # Должен возвращаться track
        assert isinstance(response.json().get("track"), int)