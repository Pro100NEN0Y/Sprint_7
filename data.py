import random
import string

def generate_courier_data():
    def random_string(length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    return {
        "login": random_string(),
        "password": random_string(),
        "firstName": random_string()
    }