from flask import Flask, render_template, request, url_for, redirect, flash
import tmdb_client
import random
import datetime

FAVORITES = set()

app = Flask(__name__)
app.secret_key = b'my-secret'


@app.route("/favorites/add", methods=['POST'])
def add_to_favorites():
    data = request.form
    movie_id = data.get('movie_id')
    movie_title = data.get('movie_title')
    if movie_id and movie_title:
        FAVORITES.add(movie_id)
        flash(f'Dodano film {movie_title} do ulubionych!')
    return redirect(url_for('homepage'))


@app.route('/')
def homepage():
    selected_list = request.args.get('list_type', "popular")
    movies = tmdb_client.get_movies(how_many=16, list_type=selected_list)
    buttons = [
        {'id': "upcoming",'name':'upcoming', 'active':False},
        {'id': "top_rated",'name':'top rated', 'active':False},
        {'id': "popular",'name':'popular', 'active':False},
        {'id': "now_playing",'name':'now playing', 'active':False}
    ]
    for butt in buttons:
        if butt['id'] == selected_list:
            butt['active']=True

    return render_template("homepage.html", movies=movies, buttons=buttons, list_type=selected_list)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}


@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast_val = tmdb_client.get_single_movie_cast(movie_id)
    cast = cast_val["cast"]
    movie_images = tmdb_client.get_movie_images(movie_id)
    backdrop = random.choice(movie_images['backdrops'])
    link = backdrop["file_path"]
    selected_backdrop = f'https://image.tmdb.org/t/p/w780/{link}'
    return render_template("movie_details.html", movie=details, cast=cast, picture=selected_backdrop)


@app.route('/search')
def search():
    search_query = request.args.get("q", "")
    if search_query:
        movies = tmdb_client.search(search_query=search_query)
    else:
        movies = []
    return render_template("search.html", movies=movies, search_query=search_query)


@app.route('/today')
def today():
    movies = tmdb_client.get_airing_today()
    today = datetime.date.today()
    return render_template("today.html", movies=movies, today=today)


@app.route("/favorites")
def show_favorites():
    if FAVORITES:
        movies = []
        for movie_id in FAVORITES:
            movie_details = tmdb_client.get_single_movie(movie_id)
            movies.append(movie_details)
    else:
        movies = []
    return render_template("homepage.html", movies=movies)


if __name__ == '__main__':
    print(tmdb_client.get_popular_movies())
    app.run(debug=True)

