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