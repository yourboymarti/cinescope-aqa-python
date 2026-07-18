import pytest
import requests

from clients.api_manager import ApiManager
from models.base_models import LoginResponse, RegisterUserResponse
from utils.data_generator import generate_user_data
from models.users import RegistrationUser
import logging
from pydantic import ValidationError

logger = logging.getLogger(__name__)

class TestAuth:
    def test_register_user(self, api_manager: ApiManager, registration_user_data):
        response = api_manager.auth_api.register_user(user_data=registration_user_data)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == registration_user_data.email, "Email не совпадает"

    def test_register_and_login_user(self, api_manager, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data, expected_status=201)
        login_response = LoginResponse(**response.json())

        assert login_response.accessToken
        assert login_response.user.email == registered_user["email"]

    def test_update_session_headers(self, api_manager):
        api_manager.auth_api._update_session_headers({"foo": "bar"})

        assert api_manager.auth_api.session.headers["foo"] == "bar"


    def test_register_timeout(self, api_manager, test_user):
        with pytest.raises(requests.exceptions.Timeout):
            api_manager.auth_api.register_user(test_user, timeout=0.001)


    def test_register_and_delete_users(self, api_manager, authenticated_user):
        user_ids = []

        for _ in range(3):
            unique_user_data = generate_user_data()
            response = api_manager.auth_api.register_user(unique_user_data)
            register_user_response = RegisterUserResponse(**response.json())
            user_ids.append(register_user_response.id)

        api_manager.user_api.delete_users(*user_ids)

    def test_validate_user_models(self, test_user, creation_user_data):
        validated_test_user = RegistrationUser(**test_user.model_dump(exclude_unset=True))
        validated_creation_user = RegistrationUser(**creation_user_data)

        test_user_json = validated_test_user.model_dump_json(exclude_unset=True)
        creation_user_json = validated_creation_user.model_dump_json()

        logger.info(f"test_user_json: {test_user_json}")
        logger.info(f"creation_user_json: {creation_user_json}")

    def test_validate_user_model_with_invalid_email(self, test_user):
        invalid_user_data = test_user.model_dump()
        invalid_user_data["email"] = "invalid-email"

        with pytest.raises(ValidationError):
            RegistrationUser(**invalid_user_data)
