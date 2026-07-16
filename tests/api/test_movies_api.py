import os
from dotenv import load_dotenv
from utils.data_generator import generate_movie_data, generate_movie_update_data

load_dotenv()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

class TestMoviesApi:
    def test_get_all_movies(self, api_manager):
        response = api_manager.movies_api.get_all_movies()
        response_data = response.json()

        assert response.status_code == 200
        assert "movies" in response_data


    def test_create_movie(self, created_movie):
        movie_data, movie = created_movie

        assert "id" in movie
        assert movie["name"] == movie_data["name"]
        assert movie["price"] == movie_data["price"]


    def test_create_movie_with_invalid_data(self, super_admin):
        movie_data = generate_movie_data()
        del movie_data["price"]

        response = super_admin.api.movies_api.create_movie(movie_data, expected_status=400)

        assert response.status_code == 400


    def test_get_movie_by_invalid_id(self, super_admin):
        response = super_admin.api.movies_api.get_movie_by_id(0, expected_status=404)

        assert response.status_code == 404


    def test_get_movie_by_id(self, api_manager, created_movie):
        movie_data, movie = created_movie

        response = api_manager.movies_api.get_movie_by_id(movie["id"])
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["id"] == movie["id"]
        assert response_data["name"] == movie_data["name"]


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


    def test_delete_movie_by_id(self, api_manager, super_admin, created_movie):
        _, movie = created_movie
        response = super_admin.api.movies_api.delete_movie_by_id(movie["id"])

        assert response.status_code == 200

        get_response = api_manager.movies_api.get_movie_by_id(movie["id"], expected_status=404)
        assert get_response.status_code == 404


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



    def test_common_user_cannot_create_movie(self, common_user):
        movie_data = generate_movie_data()
        response = common_user.api.movies_api.create_movie(movie_data, expected_status=403)

        assert response.status_code == 403


