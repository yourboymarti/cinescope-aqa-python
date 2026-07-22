import allure
import pytest
from utils.data_generator import generate_movie_data, generate_movie_update_data
from models.base_models import MoviesResponse


@allure.epic("Movies")
@allure.feature("Тестирование получение, создание, удаление и обновление фильмов")
@pytest.mark.api
@pytest.mark.regression
class TestMoviesApi:

    @allure.story("Корректность получение фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения всех фильмов")
    @pytest.mark.smoke
    def test_get_all_movies(self, api_manager):
        response = api_manager.movies_api.get_all_movies()

        movies_response = MoviesResponse(**response.json())

        assert response.status_code == 200
        assert isinstance(movies_response.movies, list)

    @allure.story("Корректность создания фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест создания фильма")
    @pytest.mark.smoke
    def test_create_movie(self, created_movie):
        movie_data, movie = created_movie

        assert "id" in movie
        assert movie["name"] == movie_data["name"]
        assert movie["price"] == movie_data["price"]

    @allure.story("Корректность создания фильмов")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Тест создания фильма с некорректным телом запроса")
    def test_create_movie_with_invalid_data(self, super_admin):
        movie_data = generate_movie_data()
        del movie_data["price"]

        response = super_admin.api.movies_api.create_movie(movie_data, expected_status=400)

        assert response.status_code == 400

    @allure.story("Корректность получение фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения фильма по невалидному id")
    def test_get_movie_by_invalid_id(self, super_admin):
        response = super_admin.api.movies_api.get_movie_by_id(0, expected_status=404)

        assert response.status_code == 404

    @allure.story("Корректность получение фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения фильма по id")
    @pytest.mark.smoke
    def test_get_movie_by_id(self, api_manager, created_movie):
        movie_data, movie = created_movie

        response = api_manager.movies_api.get_movie_by_id(movie["id"])
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["id"] == movie["id"]
        assert response_data["name"] == movie_data["name"]

    @allure.story("Корректность обновления фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест обновления фильма по id")
    def test_update_movie_by_id(self, super_admin, created_movie):
        movie_data, movie = created_movie
        update_data = generate_movie_update_data()

        response = super_admin.api.movies_api.update_movie_by_id(
            movie["id"],
            update_data
        )
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["name"] == update_data["name"]
        assert response_data["price"] == update_data["price"]

    @allure.story("Корректность удаления фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест удаления фильма по id")
    def test_delete_movie_by_id(self, api_manager, super_admin, created_movie):
        _, movie = created_movie
        response = super_admin.api.movies_api.delete_movie_by_id(movie["id"])

        assert response.status_code == 200

        get_response = api_manager.movies_api.get_movie_by_id(movie["id"], expected_status=404)
        assert get_response.status_code == 404

    @allure.story("Корректность получение фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения фильма по location")
    def test_get_movies_by_location(self, api_manager, created_movie):
        movie_data, movie = created_movie

        params = {"locations": movie["location"]}
        response = api_manager.movies_api.get_all_movies(params=params)
        assert response.status_code == 200

        response_data = response.json()
        params["page"] = response_data["pageCount"]
        response = api_manager.movies_api.get_all_movies(params=params)
        response_data = response.json()
        movie_found = False

        for movie_from_response in response_data["movies"]:
            if movie_from_response["id"] == movie["id"]:
                movie_found = True
                assert movie_from_response["location"] == movie["location"]

        assert movie_found

    @allure.story("Корректность получение фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения фильма по genre_id")
    def test_get_movies_by_genre_id(self, api_manager, created_movie):
        movie_data, movie = created_movie

        params = {"genreId": movie["genreId"]}
        response = api_manager.movies_api.get_all_movies(params=params)

        assert response.status_code == 200

        response_data = response.json()
        params["page"] = response_data["pageCount"]
        response = api_manager.movies_api.get_all_movies(params=params)
        response_data = response.json()
        movie_found = False

        for movie_from_response in response_data["movies"]:
            if movie_from_response["id"] == movie["id"]:
                movie_found = True
                assert movie_from_response["genreId"] == movie["genreId"]

        assert movie_found

    @allure.story("Корректность получение фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения фильма по published")
    def test_get_movies_by_published(self, api_manager, created_movie):
        movie_data, movie = created_movie

        params = {"published": movie["published"]}
        response = api_manager.movies_api.get_all_movies(params=params)
        assert response.status_code == 200

        response_data = response.json()
        params["page"] = response_data["pageCount"]
        response = api_manager.movies_api.get_all_movies(params=params)
        response_data = response.json()
        movie_found = False

        for movie_from_response in response_data["movies"]:
            if movie_from_response["id"] == movie["id"]:
                movie_found = True
                assert movie_from_response["published"] == movie["published"]

        assert movie_found

    @pytest.mark.parametrize(
        "filter_name, movie_field",
        [
            ("locations", "location"),
            ("genreId", "genreId"),
            ("published", "published"),
        ]
    )
    @allure.story("Корректность получение фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения фильма по фильтрам")
    @pytest.mark.smoke
    def test_get_movies_by_filters(self, api_manager, created_movie, filter_name, movie_field):
        movie_data, movie = created_movie
        params = {filter_name: movie[movie_field]}

        response = api_manager.movies_api.get_all_movies(params=params)
        assert response.status_code == 200

        response_data = response.json()
        params["page"] = response_data["pageCount"]

        response = api_manager.movies_api.get_all_movies(params=params)
        response_data = response.json()

        movie_found = False

        for movie_from_response in response_data["movies"]:
            if movie_from_response["id"] == movie["id"]:
                movie_found = True
                assert movie_from_response[movie_field] == movie[movie_field]

        assert movie_found

    @allure.story("Корректность создания фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест создания фильма юзером")
    def test_common_user_cannot_create_movie(self, common_user):
        movie_data = generate_movie_data()
        response = common_user.api.movies_api.create_movie(movie_data, expected_status=403)

        assert response.status_code == 403

    @allure.story("Корректность создания фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест создания фильма админом")
    def test_admin_cannot_create_movie(self, admin_user):
        movie_data = generate_movie_data()
        response = admin_user.api.movies_api.create_movie(movie_data, expected_status=403)

        assert response.status_code == 403

    @allure.story("Корректность удаления фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест удаления фильма разными ролями")
    @pytest.mark.parametrize("user_fixture, expected_status",
    [
        ("super_admin", 200),
        ("admin_user", 403),
        ("common_user", 403),
    ]
                                )
    def test_delete_movie_by_role(self, request, created_movie, user_fixture, expected_status, api_manager):
        user = request.getfixturevalue(user_fixture)
        _, movie = created_movie
        response = user.api.movies_api.delete_movie_by_id(movie["id"], expected_status=expected_status)

        assert response.status_code == expected_status

        if expected_status == 200:
            get_response = api_manager.movies_api.get_movie_by_id(movie["id"], expected_status=404)
            assert get_response.status_code == 404

    @allure.story("Корректность создания и удаления фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест создания и удаления фильма по id в DB")
    @pytest.mark.slow
    def test_create_and_delete_movie_in_db(self, super_admin, db_helper):
        movie_data = generate_movie_data()
        assert db_helper.get_movie_by_name(movie_data["name"]) is None

        response = super_admin.api.movies_api.create_movie(movie_data)
        movie = response.json()
        assert response.status_code == 201

        try:
            assert db_helper.movie_exists_by_id(movie["id"]) is True
            movie_from_db = db_helper.get_movie_by_id(movie["id"])

            assert movie_from_db.name == movie_data["name"]
            assert movie_from_db.price == movie_data["price"]
            assert movie_from_db.description == movie_data["description"]

        finally:
            delete_response = super_admin.api.movies_api.delete_movie_by_id(movie["id"])
            assert delete_response.status_code == 200

        assert db_helper.get_movie_by_id(movie["id"]) is None

    @allure.story("Корректность обновления фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест обновления фильма по id в DB")
    @pytest.mark.slow
    def test_update_movie_in_db(self, super_admin, db_helper, created_movie):

        movie_data, movie = created_movie
        update_data = generate_movie_update_data()

        movie_from_db = db_helper.get_movie_by_id(movie["id"])
        assert movie_from_db is not None

        response = super_admin.api.movies_api.update_movie_by_id(movie["id"], update_data)
        assert response.status_code == 200
        db_helper.db_session.expire_all()

        db_movie_after_update = db_helper.get_movie_by_id(movie["id"])
        assert db_movie_after_update is not None
        assert db_movie_after_update.name == update_data["name"]
        assert db_movie_after_update.price == update_data["price"]
        assert db_movie_after_update.description == update_data["description"]

    @allure.story("Корректность получения фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения фильма из БД по id")
    @pytest.mark.slow
    def test_movie_genre_id_in_db(self, db_helper, created_movie):

        movie_data, movie = created_movie

        movie_from_db = db_helper.get_movie_by_id(movie["id"])
        assert movie_from_db is not None
        assert movie_from_db.genre_id == movie_data["genreId"]

    @allure.story("Корректность удаления фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест удаления фильма по id в DB")
    @pytest.mark.slow
    def test_deleted_movie_absent_in_db(self, super_admin, db_helper, created_movie):

        movie_data, movie = created_movie

        movie_from_db = db_helper.get_movie_by_id(movie["id"])
        assert movie_from_db is not None

        response = super_admin.api.movies_api.delete_movie_by_id(movie["id"])
        assert response.status_code == 200

        movie_not_in_db = db_helper.get_movie_by_id(movie["id"])
        assert movie_not_in_db is None


    @allure.story("Корректность получения фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест получения фильма по айди и проверка статуса публикации")
    @pytest.mark.slow
    def test_movie_published_status_in_db(self, db_helper, created_movie):

        movie_data, movie = created_movie

        movie_from_db = db_helper.get_movie_by_id(movie["id"])
        assert movie_from_db is not None
        assert movie_from_db.published == movie_data["published"]
