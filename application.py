from flask import Flask, redirect, request, render_template, send_from_directory, url_for, Response, abort, flash, session
from utils import runScript, insertData, getData, User, getLoggedInUser, currentTime
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from urllib.parse import urlparse, urljoin
from passlib.hash import pbkdf2_sha256
import sys

# config
app = Flask(__name__, static_url_path='')
app.config.update(
    DEBUG=True,
    SECRET_KEY=b'\xfbs:/\x13\xd2\x83U\xa5\xabf\x85\xcc\x86\x8e\xbd'
)

# Flask login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Server
@app.route('/')
def redirToHomePage():
    return redirect(url_for('homePage'))


@app.route('/Homepage')
def homePage():
    genres = getData('getAllGenreNames.sql')
    linkParams = request.args
    genrePrams = []
    for key in linkParams:
        if key != 'titleSearch' and linkParams[key] == 'on':
            genrePrams.append(key)
    for _ in range(0, 12-len(genrePrams)):
        genrePrams.append('')
    titleParam = '%{}%'.format(linkParams.get('titleSearch'))
    searchResult = getData('filmSearch.sql', titleParam, *genrePrams)
    # print(genrePrams, file=sys.stderr)
    return render_template('index.html', user=getLoggedInUser(), genres=genres, searchResult=searchResult)


@app.route('/Movie details/<path:filmTitle>')
def movieDetails(filmTitle):
    movieDetails = getData('getMovieDetails.sql', filmTitle)[0]
    movieRoles = getData('getMovieRoles.sql', filmTitle)
    movieGenres = getData('getMovieGenres.sql', filmTitle)
    reviews = getData('getReviews.sql', filmTitle)
    user = getLoggedInUser()
    userHasReview = True if user and [row for row in reviews if user.id == row[4]] else False
    next = request.path
    return render_template('movieDetails.html', user=user, pageTitle=filmTitle, movieDetails=movieDetails,
                           movieRoles=movieRoles, movieGenres=movieGenres, next=next, reviews=reviews, userHasReview=userHasReview)


@app.route('/Login')
def login():
    next = get_redirect_target()
    return render_template('login.html', next=next)

# somewhere to logout
@app.route('/logout')
@login_required
def logout():
    session.pop('_flashes', None)
    logout_user()
    return redirect_back('homePage')


@app.route('/Login/process', methods=['POST'])
def processLogin():
    email = request.form['email']
    password = request.form['password']
    user = load_user(email)
    if user and pbkdf2_sha256.verify(password, user.password):
        login_user(user)
        return redirect_back('homePage')
    else:
        return abort(401)


@app.route('/Register/process', methods=['POST'])
def processRegister():
    username = request.form['username']
    email = request.form['email']
    password = pbkdf2_sha256.hash(request.form['password'])
    gender = request.form['gender']
    birthday_day = request.form['day']
    birthday_month = request.form['month']
    birthday_year = request.form['year']
    birdthday = '{}-{}-{}'.format(birthday_year, birthday_month, birthday_day)
    country = request.form['country']
    if getData('getUserData.sql', email):
        return Response('<p>User already exists.</p>')
    insertData('insertUser.sql', (username, email,
                                  password, birdthday, gender, country))
    return redirect(url_for('homePage'))


@app.route('/addReview', methods=['POST'])
@login_required
def addReview():
    movieTitle = request.form['movieTitle']
    rating = request.form['rating']
    reviewText = request.form['review-text']
    movieID = getData('getMovieID.sql', movieTitle)
    user = getLoggedInUser()
    if not movieID:
        return abort(422)
    insertData('insertReview.sql', (movieID[0][0], user.id, rating, reviewText, currentTime(), ''))
    return redirect_back(url_for('homePage'))

@app.route('/deleteReview', methods=['POST'])
@login_required
def deleteReview():
    movieTitle = request.form['movieTitle']
    user_id = request.form['user_id']
    getData('deleteReview.sql', user_id, movieTitle)
    return redirect_back(url_for('homePage'))

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

def redirect_back(endpoint, **values):
    try:
        target = request.form['next']
    except:
        target = request.referrer
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(email):
    return User.get(email)

# handle Unprocessable Entity
@app.errorhandler(422)
def Unprocessable_Entity (e):
    return Response('<p>The request was well-formed but was unable to be followed due to semantic errors.</p>')


@app.route('/css/<path:path>')
def serve_css(path):
    return send_from_directory('css', path)


@app.route('/js/<path:path>')
def serve_js(path):
    return send_from_directory('js', path)


@app.route('/images/<path:path>')
def serve_images(path):
    return send_from_directory('images', path)


if __name__ == '__main__':
    app.run()
