"""Utility file to seed ratings database from MovieLens data in seed_data/"""


from model import User, Movie
# from model import Rating
# from model import Movie

from model import connect_to_db, db
from server import app
from time import strptime



def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    print "Movies"
    #When you start the movie load, clear out any movies from a previous load
    Movie.query.delete()

    #Read u.movie file and insert data
    for row in open("seed_data/u.item"):
        row = row.rstrip()
        row_list = row.split("|")

        movie_id, movie_title, released_at, nonsense, imdb_url = row_list[0:5]
        movie_title = movie_title[:-7]
        print movie_id
        print "before edit", released_at
        released_at = released_at.strip('-')            #strip not working
        print "after stripping", released_at

        released_at = strptime(released_at, "%d%b%y")   #TimeDate not in correct formate yet :)
        print "after edit", released_at

        movie = Movie(movie_id=movie_id, movie_title=movie_title, released_at=released_at, imdb_url=imdb_url)

        db.session.add(movie)
        break

    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
