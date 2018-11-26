from flask import *
from utils import *
import sys
app = Flask(__name__, static_url_path='')
app.debug = True


@app.route("/")
def redirToHomePage():
    return redirect(url_for('homePage'))


@app.route("/Homepage")
def homePage():
    genres = getData("getAllGenreNames.sql")
    linkParams = request.args
    genrePrams = []
    for key in linkParams:
        if key != "titleSearch" and linkParams[key] == "on":
            genrePrams.append(key)
    for _ in range(0, 12-len(genrePrams)):
        genrePrams.append("")
    titleParam = "%{}%".format(linkParams.get("titleSearch"))
    searchResult = getData("filmSearch.sql", titleParam, *genrePrams)
    # print(genrePrams, file=sys.stderr)
    return render_template("index.html", genres=genres, searchResult=searchResult)


@app.route("/Movie details/<path:filmTitle>")
def movieDetails(filmTitle):
    movieDetails = getData("getMovieDetails.sql", filmTitle)[0]
    movieRoles = getData("getMovieRoles.sql", filmTitle)
    movieGenres = getData("getMovieGenres.sql", filmTitle)
    return render_template("movieDetails.html", pageTitle=filmTitle, movieDetails=movieDetails, 
                            movieRoles=movieRoles, movieGenres=movieGenres)

# @app.route("/form", methods = ['POST', 'GET'])
# def form():
#     if request.method == 'POST':
#         result = request.form
#         return render_template("form.html", result=result, send=True)
#     else:
#         return render_template("form.html", send=False)


@app.route("/css/<path:path>")
def serve_css(path):
    return send_from_directory("css", path)


@app.route("/js/<path:path>")
def serve_js(path):
    return send_from_directory("js", path)


@app.route("/images/<path:path>")
def serve_images(path):
    return send_from_directory("images", path)


if __name__ == '__main__':
    app.run()
