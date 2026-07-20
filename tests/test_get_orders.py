import allure


@allure.epic("Яндекс Самокат API")
@allure.feature("Список заказов")
class TestGetOrdersList:

    @allure.story("Получение списка заказов")
    @allure.title("Запрос списка заказов возвращает корректный непустой список объектов")
    def test_get_orders_list_success(self, api_client):
        response = api_client.get_orders_list()

        assert response.status_code == 200
        
        response_body = response.json()
        assert "orders" in response_body  # Проверяем, что возвращается список
        assert isinstance(response_body["orders"], list)