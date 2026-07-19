import requests
import pytest
import uuid
import os
from clients.api_manager import ApiManager
from dotenv import load_dotenv

from models.base_models import TestUser
from utils.data_generator import generate_movie_data
from entities.user import User
from typing import Any
from constants.roles import Roles
from utils.data_generator import DataGenerator


load_dotenv()
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
SUPER_ADMIN_USERNAME = os.getenv("SUPER_ADMIN_USERNAME")
SUPER_ADMIN_PASSWORD= os.getenv("SUPER_ADMIN_PASSWORD")


@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)



@pytest.fixture
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]
    )

@pytest.fixture(scope="function")
def registered_user(api_manager, test_user: TestUser):
    response = api_manager.auth_api.register_user(test_user).json()

    registered_user_data = test_user.model_dump()
    registered_user_data["id"] = response["id"]

    return registered_user_data


@pytest.fixture(scope="function")
def unauthenticated_api_manager():
    http_session = requests.Session()
    yield ApiManager(http_session)
    http_session.close()


@pytest.fixture
def authenticated_user(api_manager, test_user: TestUser):
    response = api_manager.auth_api.register_user(test_user)
    user_id = response.json()["id"]

    api_manager.auth_api.authenticate((ADMIN_EMAIL, ADMIN_PASSWORD))

    return api_manager, test_user.model_dump(), user_id

@pytest.fixture
def created_movie(api_manager, super_admin):
    movie_data = generate_movie_data()
    response = super_admin.api.movies_api.create_movie(movie_data)
    movie = response.json()

    yield movie_data, movie

    try:
        super_admin.api.movies_api.get_movie_by_id(movie["id"])
    except ValueError as error:
        if "status code: 404" not in str(error):
            raise
    else:
        super_admin.api.movies_api.delete_movie_by_id(movie["id"])


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()



@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SUPER_ADMIN_USERNAME,
        SUPER_ADMIN_PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture
def creation_user_data(test_user: TestUser) -> dict[str, Any]:
    updated_data = test_user.model_dump()
    updated_data.update({
        "roles": [Roles.USER.value],
        "verified": True,
        "banned": False
    })
    return updated_data


@pytest.fixture
def creation_admin_data(test_user: TestUser) -> dict[str, Any]:
    updated_data = test_user.model_dump()
    updated_data.update({
        "roles": [Roles.ADMIN.value],
        "verified": True,
        "banned": False
    })
    return updated_data

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.USER.value],
        new_session
    )

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def admin_user(user_session, super_admin, creation_admin_data):
    new_session = user_session()

    admin_user = User(
        creation_admin_data['email'],
        creation_admin_data['password'],
        [Roles.ADMIN.value],
        new_session
    )
    super_admin.api.user_api.create_user(creation_admin_data)
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user


@pytest.fixture
def registration_user_data() -> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]
    )
