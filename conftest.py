import requests
import pytest
from clients.api_manager import ApiManager
from config.credentials import ADMIN_EMAIL, ADMIN_PASSWORD
# from utils.data_generator import DataGenerator


@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)


import uuid
import pytest


@pytest.fixture(scope="function")
def test_user():
    password = "12345678Aa"
    short_id = uuid.uuid4().hex[:8]

    return {
        "email": f"test_{short_id}@mail.com",
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

