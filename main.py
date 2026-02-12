from flask import Flask, render_template, request, session, redirect, abort
import db
import os
from werkzeug.utils import secure_filename




app = Flask(__name__)
app.secret_key = "gtg"

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    sort = request.args.get("sort", "watched")
    min_rating = request.args.get("min_rating", "").strip()
    user = request.args.get("user", "").strip()

    min_rating_int = int(min_rating) if min_rating.isdigit() else None
    user_val = user if user else None

    reviews = db.get_reviews_filtered(sort=sort, min_rating=min_rating_int, username=user_val)

    user_id = session.get("id")
    reviews = [dict(r) for r in reviews]
    for r in reviews:
        r["can_edit"] = (user_id is not None and r["user_id"] == user_id)

    return render_template(
        "index.html",
        reviews=reviews,
        sort=sort,
        min_rating=min_rating_int,
        user=user
    )



@app.route("/")
def Home():
    """
    IMPORTANT:
    We DO NOT use db.GetAllReviews() here because it doesn't return Reviews.id or Reviews.user_id.
    We fetch what the template needs (id + user_id) and also compute can_edit safely.
    """
    conn = db.GetDB()
    rows = conn.execute("""SELECT
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
        ORDER BY Reviews.review_date DESC
    """).fetchall()
    conn.close()

    current_user_id = session.get("id")

    # Convert sqlite3.Row -> dict + add can_edit
    reviews = []
    for r in rows:
        item = dict(r)
        item["can_edit"] = (current_user_id is not None and item["user_id"] == current_user_id)
        reviews.append(item)

    return render_template("index.html", reviews=reviews)


@app.route("/login", methods=["GET", "POST"])
def Login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = db.CheckLogin(username, password)
        if user:
            session["username"] = user["username"]
            session["id"] = user["id"]
            return redirect("/")

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def Register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if db.RegisterUser(username, password):
            return redirect("/")

    return render_template("register.html")


@app.route("/add", methods=["GET", "POST"])
def Add():
    if session.get("id") is None:
        return redirect("/login")

    if request.method == "POST":
        user_id = session["id"]
        review_date = request.form["review_date"]
        movie_title = request.form["movie_title"]
        rating = request.form["rating"]
        review_text = request.form["review_text"]

        poster_filename = None
        if "poster" in request.files:
            poster = request.files["poster"]
            if poster and poster.filename != "" and allowed_file(poster.filename):
                safe_name = secure_filename(poster.filename)
                poster_filename = f"user{user_id}_{safe_name}"
                poster.save(os.path.join(app.config["UPLOAD_FOLDER"], poster_filename))

        db.AddReview(user_id, review_date, movie_title, rating, review_text, poster_filename)
        return redirect("/")

    return render_template("add.html")


@app.route("/review/<int:review_id>/edit", methods=["GET", "POST"])
def edit_review(review_id):
    if not session.get("id"):
        return redirect("/login")

    conn = db.GetDB()
    review = conn.execute("""
        SELECT * FROM Reviews
        WHERE id = ? AND user_id = ?
    """, (review_id, session["id"])).fetchone()

    if review is None:
        conn.close()
        abort(403)

    if request.method == "POST":
        review_date = request.form.get("review_date", review["review_date"])
        movie_title = request.form["movie_title"]
        rating = request.form["rating"]
        review_text = request.form["review_text"]

        # Optional: poster replacement
        poster_filename = review["poster_filename"]
        if "poster" in request.files:
            poster = request.files["poster"]
            if poster and poster.filename != "" and allowed_file(poster.filename):
                safe_name = secure_filename(poster.filename)
                poster_filename = f"user{session['id']}_{safe_name}"
                poster.save(os.path.join(app.config["UPLOAD_FOLDER"], poster_filename))

        conn.execute("""
            UPDATE Reviews
            SET review_date = ?,
                movie_title = ?,
                rating = ?,
                review_text = ?,
                poster_filename = ?
            WHERE id = ? AND user_id = ?
        """, (
            review_date,
            movie_title.strip(),
            rating,
            review_text.strip(),
            poster_filename,
            review_id,
            session["id"]
        ))
        conn.commit()
        conn.close()
        return redirect("/")

    conn.close()
    return render_template("edit.html", review=review)


@app.route("/review/<int:review_id>/delete", methods=["POST"])
def delete_review(review_id):
    if not session.get("id"):
        return redirect("/login")

    conn = db.GetDB()
    conn.execute("""
        DELETE FROM Reviews
        WHERE id = ? AND user_id = ?
    """, (review_id, session["id"]))
    conn.commit()

    if conn.total_changes == 0:
        conn.close()
        abort(403)

    conn.close()
    return redirect("/")


@app.route("/review/<int:review_id>")
def view_review(review_id):
    review = db.get_review_by_id(review_id)

    if not review:
        return "Review not found", 404

    return render_template("view.html", review=review)



if __name__ == "__main__":
    app.run(debug=True, port=5000)
