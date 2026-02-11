from flask import Flask, render_template, request, session, redirect
import db

import os
from werkzeug.utils import secure_filename

from flask import abort


app = Flask(__name__)
app.secret_key = "gtg"

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def Home():
    reviewData = db.GetAllReviews()
    return render_template("index.html", reviews=reviewData)

@app.route("/login", methods=["GET", "POST"])
def Login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = db.CheckLogin(username, password)
        if user:
            session['username'] = user['username']
            session['id'] = user['id'] 
            return redirect("/")

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def Register():

    # If they click the submit button, let's register
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Try and add them to the DB
        if db.RegisterUser(username, password):
            # Success! Let's go to the homepage
            return redirect("/")

    return render_template("register.html")



@app.route("/add", methods=["GET", "POST"])
def Add():
    if session.get('id') is None:
        return redirect("/login")

    if request.method == "POST":
        user_id = session['id']
        review_date = request.form['review_date']
        movie_title = request.form['movie_title']
        rating = request.form['rating']
        review_text = request.form['review_text']

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
        abort(403)

    conn = db.GetDB()
    review = conn.execute("""
        SELECT * FROM Reviews
        WHERE id = ? AND user_id = ?
    """, (review_id, session["id"])).fetchone()

    if review is None:
        conn.close()
        abort(403)

    if request.method == "POST":
        conn.execute("""
            UPDATE Reviews
            SET movie_title = ?, rating = ?, review_text = ?
            WHERE id = ? AND user_id = ?
        """, (
            request.form["movie_title"],
            request.form["rating"],
            request.form["review_text"],
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
        abort(403)

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



app.run(debug=True, port=5000)