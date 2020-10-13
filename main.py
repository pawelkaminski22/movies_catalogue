from flask import Flask, render_template
import requests
import tmdb_client
import tbdb_client


app = Flask(__name__)

@app.route('/')
def homepage():
    movies = []
    return render_template("homepage.html", movies=movies)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}


if __name__ == '__main__':
    print(tmdb_client.get_popular_movies())
    #app.run(debug=True)

