import uuid
from faker import Faker

faker = Faker()

def generate_user_data() -> dict:
    short_id = uuid.uuid4().hex[:8]
    password = "12345678Aa"

    return {
        "email": f"test_{short_id}@mail.com",
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
