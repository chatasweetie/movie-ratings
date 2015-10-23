"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "12345catsarecats"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/login', methods=["POST"])
def login():
    email = request.form.get("email")
    print "email: ", email
    password = request.form.get("password")
    print "password: ", password

    query = User.query.filter(User.email == email).first()
    print query
    if query is None:
        #Let the user know that its bad email
        print "I'm not in the data base"
        flash("Your email is incorrect or not in the system") 
        return redirect(".")
    else:
        if password != query.password:
            print "Incorrect password"
            flash("Your password is incorrect.")
            return redirect(".")
        else:
            print "Log In complete!"
            flash("Logged in successfully!")
            session['session_email'] = email
            print session
            return redirect('/')
       

@app.route('/logout', methods=["POST"])
def logout():
    """Logs the user out of the system"""
    del session['session_email']
    flash("You're logged out")

    return redirect("/")


@app.route('/users')
def user_list():
    """Show a list of the users"""

    users = User.query.all()

    return render_template('user_list.html', users=users)


@app.route('/check_create_user', methods=["GET"])
def create_user():
    """loads the create user form """
    return render_template('create_user.html')


def insert_user(email, password, zipcode, age):
    """adds user to database and commits"""
    user = User(email=email, password=password, zipcode=zipcode, age=age)

    db.session.add(user)

    db.session.commit()


@app.route('/check_create_user', methods=["POST"])
def check_create_user():
    """Creates a user login with email and password and stores it in the users table."""

    email = request.form.get("email")
    password = request.form.get("password")
    zipcode = request.form.get("zipcode")
    age = request.form.get("age")

    print email, password, zipcode, age
    # Check if user already has a login with that email address
    query = User.query.filter(User.email == email).first()
    if query:
        print "That user already has an email associated with a login"
        flash("You've already got a login.  Try to remember your password!")
    else:
        insert_user(email, password, zipcode, age)
    return redirect('.') 


@app.route('/movies')
def list_movies():
    """Creates a list of movies in the database that can be reviewed."""

    movies = Movie.query.order_by(Movie.movie_title).all()
    print movies

    return render_template("movie_list.html", movies=movies)


@app.route('/movie/<int:movie_id>')
def list_movie_details(movie_id):
    """ Show a detailed profile page of a movie and all ratings associated with that movie.
    If user is logged in, 'Rate This Movie' button will appear."""
    print "movie id", movie_id

    movie_to_show = Movie.query.filter(Movie.movie_id == movie_id).first()
    print "to show", movie_to_show
    return render_template("movie_details.html", movie_to_show=movie_to_show)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()