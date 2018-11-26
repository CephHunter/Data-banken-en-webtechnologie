from flask import *
from utils import *
import sys
app = Flask(__name__, static_url_path='')
app.debug = True

@app.route("/")
def redirToHomePage():
    return redirect(url_for('homePage'))

@app.route("/Homepage", methods = ['POST', 'GET'])
def homePage():
    genres = getData("getAllGenreNames.sql")
    linkParams = request.args
    searchResult = getData("filmSearch.sql")
    return render_template("index.html", genres=genres, linkParams=linkParams, searchResult=searchResult)

@app.route("/form", methods = ['POST', 'GET'])
def form():
    if request.method == 'POST':
        result = request.form 
        return render_template("form.html", result=result, send=True)
    else:
        return render_template("form.html", send=False)

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
