import requests
import pytest
import uuid
import os
from clients.api_manager import ApiManager
from dotenv import load_dotenv
from utils.data_generator import generate_movie_data

load_dotenv()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)



@pytest.fixture(scope="function")
def test_user():
    password = "12345678Aa"
    short_id = uuid.uuid4().hex[:8]

    return {
        "email": f"test{short_id}@gmail.com",
        "fullName": "Test User",
        "password": password,
        "passwordRepeat": password,
        "roles": ["ADMIN"]
    }

@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user).json()
    test_user["id"] = response["id"]

    return test_user





@pytest.fixture(scope="function")
def unauthenticated_api_manager():
    http_session = requests.Session()
    yield ApiManager(http_session)
    http_session.close()



@pytest.fixture
def authenticated_user(api_manager, test_user):
    # Шаг 1: регистрация
    response = api_manager.auth_api.register_user(test_user)
    user_id = response.json()["id"]

    # Шаг 2: логин/аутентификация
    api_manager.auth_api.authenticate((ADMIN_EMAIL, ADMIN_PASSWORD))

    # Шаг 3: возвращаем всё, что нужно тесту
    return api_manager, test_user, user_id



@pytest.fixture
def created_movie(api_manager):
    api_manager.auth_api.authenticate((ADMIN_EMAIL, ADMIN_PASSWORD))

    movie_data = generate_movie_data()
    response = api_manager.movies_api.create_movie(movie_data)
    movie = response.json()

    yield movie_data, movie

    try:
        api_manager.movies_api.get_movie_by_id(movie["id"])
    except ValueError as error:
        if "status code: 404" not in str(error):
            raise
    else:
        api_manager.movies_api.delete_movie_by_id(movie["id"])
