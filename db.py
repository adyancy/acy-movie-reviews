import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash



def GetDB():
    # Connect to the database and return the connection object
    db = sqlite3.connect(".database/gtg.db")
    db.row_factory = sqlite3.Row
    return db


def GetAllReviews():
    # Connect, query all reviews and then return the data
    db = GetDB()

    reviews = db.execute("""
        SELECT Reviews.review_date,
               Reviews.movie_title,
               Reviews.rating,
               Reviews.review_text,
               Reviews.poster_filename,
               Users.username
        FROM Reviews
        JOIN Users ON Reviews.user_id = Users.id
        ORDER BY Reviews.review_date DESC
    """).fetchall()

    db.close()
    return reviews



def CheckLogin(username, password):
    db = GetDB()
    user = db.execute(
        "SELECT * FROM Users WHERE username=? COLLATE NOCASE",
        (username,)
    ).fetchone()
    db.close()

    if user is not None and check_password_hash(user['password'], password):
        return user

    return None



def RegisterUser(username, password):
    # Check if they gave us a username and password
    if username is None or password is None:
        return False

    # Attempt to add them to the database
    db = GetDB()
    hash = generate_password_hash(password)
    db.execute("INSERT INTO Users(username, password) VALUES(?, ?)", (username, hash))
    db.commit()
    db.close()
    return True

def AddReview(user_id, review_date, movie_title, rating, review_text, poster_filename):

    if not user_id or not review_date or not movie_title or not review_text:
        return False

    try:
        rating = int(rating)
    except:
        return False

    if rating < 1 or rating > 5:
        return False

    db = GetDB()
    db.execute(
        "INSERT INTO Reviews(user_id, review_date, movie_title, rating, review_text, poster_filename) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, review_date, movie_title.strip(), rating, review_text.strip(), poster_filename)
    )
    db.commit()
    db.close()
    return True

