"""Utility file to seed ratings database from MovieLens data in seed_data/"""


from model import User, Movie
# from model import Rating
# from model import Movie

from model import connect_to_db, db
from server import app
from datetime import datetime



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

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def load_movies():
    """Load movies from u.item into database."""

    print "Movies"
    #When you start the movie load, clear out any movies from a previous load
    Movie.query.delete()

    #Read u.movie file and insert data
    for row in open("seed_data/u.item"):
        row = row.rstrip()
        row_list = row.split("|")

        #Check the ID
        if is_number(row_list[0]) == True:
            movie_id = int(row_list[0])
        else:
            print "That ain't no numba"
            continue

        # if int(row_list[0]):
        #     movie_id = int(row_list[0])
        #     print "the movie id: ", movie_id
        # else:
        #     continue


        #Check the datetime format

        if len(row_list[2]) != 11:
            continue## there is a way to tell it to skip this iternation and continue for loop
        else:
            released_at = row_list[2]

        #TODO: Check if the movie title and date is already in the database
            # check_movie = Movie.query.filter(Movie.movie_title == row_list[1]).first()
            # if check_movie != None:
            #     continue## there is a way to tell it to skip this iternation and continue for loop
            #     print "Move already in here ", row_list[1]
            # else:
            #     movie_title = row_list[1]
            #     movie_title = movie_title[:-7]
        
        movie_title = row_list[1]
        movie_title = movie_title[:-7]
        
        imdb_url = row_list[4]
        

        released_datetime = datetime.strptime(released_at, "%d-%b-%Y")              #made a datetime object
        
        movie = Movie(movie_id=movie_id, movie_title=movie_title, released_datetime=released_datetime, imdb_url=imdb_url)

        db.session.add(movie)

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
