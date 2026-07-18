import pytest
import requests
from utils.data_generator import generate_user_data
from models.users import RegistrationUser
import logging
from pydantic import ValidationError

logger = logging.getLogger(__name__)

class TestAuth:
    def test_register_user(self, api_manager, test_user):
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        assert response_data["email"] == test_user["email"]
        # добавим еше проверок
        assert "id" in response_data 
        assert "USER" in response_data["roles"]

    def test_register_and_login_user(self, api_manager, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        assert "accessToken" in response_data
        assert response_data["user"]["email"] == registered_user["email"]

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
            user_id = response.json()["id"]
            user_ids.append(user_id)

        api_manager.user_api.delete_users(*user_ids)

    def test_validate_user_models(self, test_user, creation_user_data):
        validated_test_user = RegistrationUser(**test_user)
        validated_creation_user = RegistrationUser(**creation_user_data)

        test_user_json = validated_test_user.model_dump_json(exclude_unset=True)
        creation_user_json = validated_creation_user.model_dump_json()

        logger.info(f"test_user_json: {test_user_json}")
        logger.info(f"creation_user_json: {creation_user_json}")

    def test_validate_user_model_with_invalid_email(self, test_user):
        test_user["email"] = "invalid-email"

        with pytest.raises(ValidationError):
            RegistrationUser(**test_user)
