from models.base_models import UnauthorizedResponse, UserInfoResponse, UserResponse


class TestUser:
    def test_get_user_info_without_authorization(
        self,
        unauthenticated_api_manager,
        registered_user
    ):
        response = unauthenticated_api_manager.user_api.get_user_info(
            user_id=registered_user["id"],
            expected_status=401
        )

        error_response = UnauthorizedResponse(**response.json())

        assert response.status_code == 401
        assert error_response.message == "Unauthorized"

    def test_get_user_info(self, authenticated_user):
        api_manager, test_user, user_id = authenticated_user

        response = api_manager.user_api.get_user_info(user_id)

        user_info_response = UserInfoResponse(**response.json())

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert user_info_response.email == test_user["email"]

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data).json()
        create_user_response = UserResponse(**response)

        assert create_user_response.id, "ID должен быть не пустым"
        assert create_user_response.email == creation_user_data['email']
        assert create_user_response.fullName == creation_user_data['fullName']
        assert [role.value for role in create_user_response.roles] == creation_user_data['roles']
        assert create_user_response.verified is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        response_by_id = super_admin.api.user_api.get_user(created_user_response['id']).json()
        response_by_email = super_admin.api.user_api.get_user(creation_user_data['email']).json()
        user_by_id = UserResponse(**response_by_id)
        user_by_email = UserResponse(**response_by_email)

        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert user_by_id == user_by_email, "Содержание ответов должно быть идентичным"
        assert user_by_id.id, "ID должен быть не пустым"
        assert user_by_id.email == creation_user_data['email']
        assert user_by_id.fullName == creation_user_data['fullName']
        assert [role.value for role in user_by_id.roles] == creation_user_data['roles']
        assert user_by_id.verified is True

    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)
