from config.credentials import ADMIN_EMAIL, ADMIN_PASSWORD
from utils.data_generator import generate_movie_data, generate_movie_update_data

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


    def test_get_movie_by_id(self, api_manager, created_movie):
        movie_data, movie = created_movie

        response = api_manager.movies_api.get_movie_by_id(movie["id"])
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["id"] == movie["id"]
        assert response_data["name"] == movie_data["name"]


    def test_update_movie_by_id(self, api_manager, created_movie):
        movie_data, movie = created_movie
        update_data = generate_movie_update_data()

        response = api_manager.movies_api.update_movie_by_id(
            movie["id"],
            update_data
        )
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["name"] == update_data["name"]
        assert response_data["price"] == update_data["price"]


    def test_delete_movie_by_id(self, api_manager):
        api_manager.auth_api.authenticate((ADMIN_EMAIL, ADMIN_PASSWORD))
        movie_data = generate_movie_data()
        movie = api_manager.movies_api.create_movie(movie_data).json()

        response = api_manager.movies_api.delete_movie_by_id(movie["id"])

        assert response.status_code == 200

        get_response = api_manager.movies_api.get_movie_by_id(movie["id"], expected_status=404)
        assert get_response.status_code == 404


    def test_get_movies_by_location(self, api_manager, created_movie):
        movie_data, movie = created_movie

        response = api_manager.movies_api.get_all_movies(
            params={"locations": movie["location"]}
        )
        assert response.status_code == 200

        response_data = response.json()

        for movie_from_response in response_data["movies"]:
            assert movie_from_response["location"] == movie["location"]


    def test_get_movies_by_genre_id(self, api_manager, created_movie):
        movie_data, movie = created_movie

        response = api_manager.movies_api.get_all_movies(params={"genreId": movie["genreId"]})

        assert response.status_code == 200

        response_data = response.json()

        for movie_from_response in response_data["movies"]:
            assert movie_from_response["genreId"] == movie["genreId"]


    def test_get_movies_by_published(self, api_manager, created_movie):
        movie_data, movie = created_movie

        response = api_manager.movies_api.get_all_movies(params={"published": movie["published"]})
        assert response.status_code == 200

        response_data = response.json()
        for movie_from_response in response_data["movies"]:
            assert movie_from_response["published"] == movie["published"]




