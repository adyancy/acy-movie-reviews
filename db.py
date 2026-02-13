import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


def GetDB():
    # Connect to the database and return the connection object
    db = sqlite3.connect(".database/gtg.db")
    db.row_factory = sqlite3.Row
    return db


def GetAllReviews():
    db = GetDB()

    reviews = db.execute("""
        SELECT Reviews.id   AS review_id,
               Reviews.user_id,
               Reviews.review_date,
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

def GetReviewById(review_id):
    db = GetDB()
    review = db.execute("""
        SELECT * FROM Reviews WHERE id = ?
    """, (review_id,)).fetchone()
    db.close()
    return review


def UpdateReview(review_id, user_id, review_date, movie_title, rating, review_text, poster_filename=None):
    # Only update if it belongs to the user_id
    db = GetDB()

    try:
        rating = int(rating)
    except:
        return False
    if rating < 1 or rating > 5:
        return False

    if poster_filename:
        db.execute("""
            UPDATE Reviews
               SET review_date=?,
                   movie_title=?,
                   rating=?,
                   review_text=?,
                   poster_filename=?
             WHERE id=? AND user_id=?
        """, (review_date, movie_title.strip(), rating, review_text.strip(), poster_filename, review_id, user_id))
    else:
        db.execute("""
            UPDATE Reviews
               SET review_date=?,
                   movie_title=?,
                   rating=?,
                   review_text=?
             WHERE id=? AND user_id=?
        """, (review_date, movie_title.strip(), rating, review_text.strip(), review_id, user_id))

    db.commit()
    rows = db.total_changes
    db.close()
    return rows > 0


def DeleteReview(review_id, user_id):
    db = GetDB()
    db.execute("DELETE FROM Reviews WHERE id=? AND user_id=?", (review_id, user_id))
    db.commit()
    rows = db.total_changes
    db.close()
    return rows > 0

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

def get_review_by_id(review_id):
    db = GetDB()
    review = db.execute("""
        SELECT
            Reviews.id AS id,
            Reviews.user_id AS user_id,
            Reviews.review_date,
            Reviews.movie_title,
            Reviews.rating,
            Reviews.review_text,
            Reviews.poster_filename,
            Users.username
        FROM Reviews
        JOIN Users ON Reviews.user_id = Users.id
        WHERE Reviews.id = ?
    """, (review_id,)).fetchone()
    db.close()
    return review

def get_reviews_filtered(sort="watched", min_rating=None, username=None):
    dbconn = GetDB()

    base = """
        SELECT
            Reviews.id AS id,
            Reviews.user_id AS user_id,
            Reviews.review_date,
            Reviews.movie_title,
            Reviews.rating,
            Reviews.review_text,
            Reviews.poster_filename,
            Users.username
        FROM Reviews
        JOIN Users ON Reviews.user_id = Users.id
    """

    where = []
    params = []

    if min_rating is not None:
        where.append("Reviews.rating >= ?")
        params.append(min_rating)

    if username:
        where.append("Users.username = ?")
        params.append(username)

    if where:
        base += " WHERE " + " AND ".join(where)

    # Sorting
    if sort == "newest":
        # "Newest posted" = highest ID (since you don't have a created_at column)
        base += " ORDER BY Reviews.id DESC"
    elif sort == "watched":
        base += " ORDER BY Reviews.review_date DESC, Reviews.id DESC"
    elif sort == "rating_desc":
        base += " ORDER BY Reviews.rating DESC, Reviews.id DESC"
    elif sort == "rating_asc":
        base += " ORDER BY Reviews.rating ASC, Reviews.id DESC"
    else:
        base += " ORDER BY Reviews.review_date DESC, Reviews.id DESC"

    rows = dbconn.execute(base, tuple(params)).fetchall()
    dbconn.close()
    return rows
