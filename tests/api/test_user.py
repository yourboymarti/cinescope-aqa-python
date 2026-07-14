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

        assert response.status_code == 401
        assert response.json()["message"] == "Unauthorized"

    def test_get_user_info(self, authenticated_user):
        api_manager, test_user, user_id = authenticated_user

        response = api_manager.user_api.get_user_info(user_id)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.json()["email"] == test_user["email"]

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data).json()

        assert response.get('id') and response['id'] != '', "ID должен быть не пустым"
        assert response.get('email') == creation_user_data['email']
        assert response.get('fullName') == creation_user_data['fullName']
        assert response.get('roles', []) == creation_user_data['roles']
        assert response.get('verified') is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        response_by_id = super_admin.api.user_api.get_user(created_user_response['id']).json()
        response_by_email = super_admin.api.user_api.get_user(creation_user_data['email']).json()

        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"
        assert response_by_id.get('email') == creation_user_data['email']
        assert response_by_id.get('fullName') == creation_user_data['fullName']
        assert response_by_id.get('roles', []) == creation_user_data['roles']
        assert response_by_id.get('verified') is True

    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)
