from flask import Flask, redirect, request, render_template, send_from_directory, url_for, Response, abort, flash, session
from utils import runScript, insertData, getData, User, getLoggedInUser, currentTime, getNextID
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


@app.route('/Movie details/<int:movieID>')
def movieDetails(movieID):
    movieDetails = getData('getMovieDetails.sql', movieID)[0]
    movieRoles = getData('getMovieRoles.sql', movieID)
    movieGenres = getData('getMovieGenres.sql', movieID)
    reviews = getData('getReviews.sql', movieID)
    user = getLoggedInUser()
    userHasReview = True if user and [
        row for row in reviews if user.id == row[4]] else False
    next = request.path
    return render_template('movieDetails.html', user=user, movieDetails=movieDetails,
                           movieRoles=movieRoles, movieGenres=movieGenres, next=next,
                           reviews=reviews, userHasReview=userHasReview)


@app.route('/Movie details/Edit/<int:movieID>')
@login_required
def editMovieDetails(movieID):
    user = getLoggedInUser()
    next = get_redirect_target()
    movieDetails = getData('getMovieDetails.sql', movieID)
    if movieDetails:
        movieDetails = movieDetails[0]
    else:
        movieDetails = ''
    movieRoles = getData('getMovieRoles.sql', movieID)
    movieGenres = [genre[0] for genre in getData('getMovieGenres.sql', movieID)]
    allGenres = getData('getAllGenreNames.sql')
    return render_template('editMovieDetails.html', next=next, user=user, movieDetails=movieDetails, movieRoles=movieRoles,
                                movieGenres=movieGenres, allGenres=allGenres)

@app.route('/addMovie')
@login_required
def addMovie():
    user = getLoggedInUser()
    next = get_redirect_target()
    nextMovieID = getNextID('movies', 'movie_id')
    return redirect('/Movie details/Edit/{}?next={}'.format(nextMovieID, next))


@app.route('/editMovie/process', methods=['POST'])
@login_required
def processEditMovieDetails():
    args = request.form
    title = args['title']
    movieID = args['movieID']
    description = args['description']
    genres = args.getlist('genres')
    releaseYear = args['release-year']
    country = args['country']
    budget = args['budget']
    nextactorID = getNextID('actors', 'actor_id')
    actorIDs = [(id or (nextactorID + i)) for i, id in enumerate(args.getlist('actor_id'))]
    actorRoles = args.getlist('role')
    actorNames = args.getlist('actor-name')
    actorGenders = args.getlist('gender')
    actorCountries = args.getlist('actor-country')
    actorBirthyear = args.getlist('birthyear')
    actorDeceaseyear = args.getlist('deceaseyear')

    if movieID:
        insertData('updateMovie.sql', (title, description, country, releaseYear, budget, '', movieID))
    else:
        movieID = getNextID('movies', 'movie_id')
        insertData('insertMovie.sql', (movieID, title, description, country, releaseYear, budget, ''))

    # Update actors
    data = [{
            'actor_id': actorIDs[i],
            'name': actorNames[i],
            'gender': actorGenders[i],
            'country': actorCountries[i],
            'year_of_birth': actorBirthyear[i],
            'year_of_decease': actorDeceaseyear[i]
        } for i in range(0, len(actorIDs))
    ]
    insertData('updateActors_1.sql', *data)
    insertData('updateActors_2.sql', *data)

    #update roles
    data = [(
            movieID,
            actorRoles[i],
            actorIDs[i]
        ) for i in range(0, len(actorIDs))
    ]
    getData('updateRoles_1.sql', movieID)
    insertData('updateRoles_2.sql', *data)

    # Update movie genres
    getData('updateGenres_1.sql', movieID)
    insertData('updateGenres_2.sql', *[(movieID, genres[i]) for i in range(0, len(genres))])

    return redirect_back('homePage')
    # return render_template('test.html', linkParams=args, title=title, description=description, genres=genres,
        # releaseYear=releaseYear, country=country, budget=budget, actorIDs=actorIDs, actorRoles=actorRoles, actorNames=actorNames,
        # actorGenders=actorGenders, actorCountries=actorCountries, actorBirthyear=actorBirthyear,
        # actorDeceaseyear=actorDeceaseyear)


@app.route('/Login')
def login():
    next = get_redirect_target()
    return render_template('login.html', next=next)


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
    rating = request.form['rating']
    reviewText = request.form['review-text']
    movieID = request.form['movieID']
    user = getLoggedInUser()
    insertData('insertReview.sql', (movieID, user.id,
                                    rating, reviewText, currentTime(), ''))
    return redirect_back(url_for('homePage'))


@app.route('/deleteReview', methods=['POST'])
@login_required
def deleteReview():
    movieID = request.form['movieID']
    user_id = request.form['user_id']
    getData('deleteReview.sql', user_id, movieID)
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
def Unprocessable_Entity(e):
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
