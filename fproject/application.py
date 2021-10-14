import os
from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fproject.db"
app.config["SESSION_TYPE"] = "filesystem"

# Initialize database
db = SQLAlchemy(app)

# Create db model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(200), nullable=False)

    # Create a function to return a string when we add something to the database
    def __repr__(self):
        return '<Username %r>' % self.username

# Login_required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

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

        # Ensure everything is filled out
        if not username or not password or not confirmation:
            return render_template("register.html", message="Please fill in all fields")

        # Ensure passwords match
        if password != confirmation:
            return render_template("register.html", message="Passwords do not match")

        # Ensure username is unique
        if db.session.query(Users).filter(Users.username == username).count() > 0:
            return render_template("register.html", message="Username already exists")

        # Add new user to database
        new_user = Users(username=username, hash=generate_password_hash(password))
        try:
            db.session.add(new_user)
            db.session.commit()
            return render_template("register.html", message="Registration successful")
        except:
            return render_template("register.html", message="Something went wrong")

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

            # Forget any user_id
            session.clear()
    
            # Ensure username was submitted
            username = request.form.get("username")
            password = request.form.get("password")
    
            # Ensure username exists and password is correct
            user = db.session.query(Users).filter(Users.username == username).first()
            if not user or not check_password_hash(user.hash, password):
                return render_template("login.html", message="Invalid username and/or password")

            # Remember which user has logged in
            session["user_id"] = user.id
    
            # Redirect user to home page
            return redirect("/") 
    else:
        return render_template("login.html")

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        # Forget any user_id
        session.clear()
        return redirect("/")
    else:
        # display username of the user
        user = db.session.query(Users).filter(Users.id == session["user_id"]).first()
        return render_template("account.html", username=user.username)
        


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


if __name__ == '__main__':
    app.debug = True
    app.run()
