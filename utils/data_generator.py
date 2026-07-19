import uuid
import datetime
from faker import Faker

faker = Faker()

class DataGenerator:

    @staticmethod
    def generate_random_password():
        return faker.password(
            length=12,
            special_chars=False,
            digits=True,
            upper_case=True,
            lower_case=True
        )

    @staticmethod
    def generate_random_email():
        return f"test{uuid.uuid4().hex[:8]}@gmail.com"


    @staticmethod
    def generate_random_name():
        return faker.name()

    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя в БД"""
        return {
            'id': f'{uuid.uuid4()}',
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }


def generate_user_data() -> dict:
    short_id = uuid.uuid4().hex[:8]
    password = "12345678Aa"

    return {
        "email": f"test{short_id}@gmail.com",
        "fullName": "Test User",
        "password": password,
        "passwordRepeat": password,
        "roles": ["ADMIN"],
    }

def generate_movie_data() -> dict:

    return {
        "name": f"{faker.word()} {uuid.uuid4().hex[:8]}",
        "imageUrl": "https://placekitten.com/300/300",
        "price": faker.random_int(min=100, max=1000),
        "description": faker.text(max_nb_chars=200),
        "location": "SPB",
        "published": True,
        "genreId": 4
    }


def generate_movie_update_data() -> dict:
    return {
        "name": f"{faker.word()} {uuid.uuid4().hex[:8]}",
        "price": faker.random_int(min=100, max=1000),
        "description": faker.text(max_nb_chars=200)
    }
