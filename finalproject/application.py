import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

# Login_required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = sqlite3.connect("project.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def redister():
    """Register user"""

    if request.method == "POST":

        # Forget any user_id
        session.clear()

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return render_template("register.html", message="Please fill in all fields")

        # Ensure passwords match
        if password != confirmation:
            return render_template("register.html", message="Passwords do not match")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", [username])

        length = rows.count(with_limit_and_skip=False)

        # Ensure username doesn't already exist
        if length != 0:
            return render_template("register.html", message="Username already exists")
        else:
            hash = generate_password_hash(password)
            # Insert data into database
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", [username], [hash])

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        pass

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "GET":
        return render_template("account.html")
    else:
        pass



