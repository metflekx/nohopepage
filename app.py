from hashlib import sha256
from lib2to3.pgen2 import driver
from tkinter import W
from unittest.util import strclass
from flask import Flask, render_template, request, session, redirect, url_for
from helpers import fail, login_required
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


# accessing database
con = sqlite3.connect("nohope.db", check_same_thread=False)
# making a cursor to for database
db = con.cursor()

app = Flask(__name__)


@app.route("/")
def index():
    # rendering home_page
    return render_template("index.html")


@app.route("/logout")
@login_required
def logout():
    # logging user out by clearing the session
    session.clear()
    return redirect("/login")


@app.route("/sign_up", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":  # checking if form was submitted
        # accessing username
        username = request.form.get("username")
        # check if username is valid
        if len(username) < 2:
            error = "username must be at least 2 letters long."
            return fail(error)
        elif not username:
            error = "please define a username."
            return fail(error)
        # checking for validation of other fields
        if request.form.get("neanderthal") == request.form.get("confirmation") and len(request.form.get("neanderthal")) >= 7:
            # accessing information
            neanderthal = generate_password_hash(
                request.form.get("neanderthal"), method="sha256")
            db.execute("INSERT INTO userinfo(username, neanderthal) VALUES(?,?)",
                       (username, neanderthal))
            con.commit()
            # redirecting user to login
            return redirect("/login")
        else:
            # throwing error
            return fail("PASSWORD doesn't match confirmation / is to short.")

    return render_template("sign_up.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    # forget user_id
    session.clear()
    # if submitting POST
    if request.method == "POST":
        # check for empty
        if not request.form.get("username") or not request.form.get("neanderthal"):
            return fail("you have to fill username and password.")

        # query database for username
        username = request.form.get("username")
        query = db.execute(
            "SELECT * FROM userinfo WHERE username = ?", (username, ))
        query = query.fetchone()

        # check if user exist and information is correct
        if not query:
            return fail("invalid username")
        elif not check_password_hash(query[2], request.form.get("neanderthal")):
            return fail("iccorect password")

        # remember wich user has logged in
        session["user_id"] = query[0]

        # redirect user to home
        return redirect("/")

    return render_template("login.html")


@app.route("/song", methods=["POST", "GET"])
def song():
    # ===========================
    # keeps track of current song
    # ===========================
    # access song title(is in url_parameter)
    song_title = request.full_path[14:]
    # keeps track of current song_id
    song_id = db.execute(
        "SELECT song_id FROM songs WHERE title = ?", (song_title, )).fetchone()[0]

    # access comments related to song
    comments = db.execute(
        "SELECT comment_message FROM comments WHERE song_id = ?", (song_id, )).fetchall()

    # checks if user posts a comments
    if request.method == "POST":
        # keeps track of comment
        comment_message = request.form.get("comment")
        # checks if comment is valid
        if not comment_message:
            return fail("you can not post an empty comment.")

        # keeps track of user who writes comment
        user_id = session["user_id"]

        # insert into comments comment_message, user_id, song_id
        db.execute(
            "INSERT INTO comments(comment_message, song_id, user_id) VALUES(?, ?, ?)", (comment_message, song_id, user_id))
        con.commit()

        # redirects user to home to avoid repeating post request

        return redirect("/")

    return render_template("song.html", comments=comments)


if __name__ == "__main__":
    app.config["SECRET_KEY"] = "fuckfuckfuck"
    app.run(debug=True)
