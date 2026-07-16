import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru"

# Эндпоинты
CREATE_COURIER_URL = f"{BASE_URL}/api/v1/courier"
LOGIN_COURIER_URL = f"{BASE_URL}/api/v1/courier/login"
DELETE_COURIER_URL = f"{BASE_URL}/api/v1/courier/"  # + id
ORDERS_URL = f"{BASE_URL}/api/v1/orders"


def generate_random_string(length=10):
    """Генерация случайной буквенной строки нижнего регистра."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_courier_data():
    """Генерация данных для нового уникального курьера."""
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }