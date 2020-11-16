import tmdb_client
from unittest.mock import Mock
from main import app


def call_tmdb_api(monkeypatch, data):
    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = data
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)
    return


def test_get_movies_list(monkeypatch):
    mock_movies_list = ['Movie 1', 'Movie 2']
    call_tmdb_api(monkeypatch, mock_movies_list)
    movies_list = tmdb_client.get_movies_list(list_type="popular")
    assert movies_list == mock_movies_list


def test_get_single_movie(monkeypatch):
    mock_movie = ['Movie 1']
    call_tmdb_api(monkeypatch, mock_movie)
    movie = tmdb_client.get_single_movie('531219')
    assert movie == mock_movie


def test_get_movie_images(monkeypatch):
    mock_image = ['Image 1']
    call_tmdb_api(monkeypatch, mock_image)
    image = tmdb_client.get_movie_images('531219')
    assert image == mock_image


def test_get_single_movie_cast(monkeypatch):
    mock_cast = ['cast']
    call_tmdb_api(monkeypatch, mock_cast)
    cast = tmdb_client.get_single_movie_cast('531219')
    assert cast == mock_cast


def test_homepage(monkeypatch):
    api_mock = Mock(return_value={'results': []})
    monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)

    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        api_mock.assert_called_once_with('movie/popular')
