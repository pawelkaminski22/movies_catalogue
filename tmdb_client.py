import requests


def get_popular_movies():
    endpoint = "https://api.themoviedb.org/3/movie/popular?api_key=53b8a7baee6070fc5f4646520e64f485&language=en-US&page=1"
    api_token = "8eb2c49656c845f346dff3b4582a86a187891b4b"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint)
    return response.json()


def get_poster_url(poster_api_path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"