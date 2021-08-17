import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

    total = db.execute("SELECT total FROM users WHERE id = ?", session["user_id"])

    data = db.execute("SELECT * FROM shares WHERE user_id = ?", session["user_id"])

    return render_template("index.html", cash=format(cash[0]['cash'], ".2f"), total=format(total[0]['total'], ".2f"), data=data)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        input = request.form.get("symbol")
        shares = request.form.get("shares")

        data = lookup(input)
        symbol = data["symbol"]
        name = data["name"]
        price = data["price"]
        total = float(shares) * price

        # Check if stock exists
        if data:
            cash = db.execute("SELECT cash FROM users WHERE id = (?)", session["user_id"])
            # Check if user has enough cash to buy stocks
            if cash[0]["cash"] < total:
                return apology("not enough cash")

            if db.execute("SELECT * FROM shares WHERE symbol = (?) AND user_id = (?)", symbol, session["user_id"]):
                # Set new amount of shares
                current_amount = db.execute("SELECT amount FROM shares WHERE symbol = (?) AND user_id = (?)", symbol, session["user_id"])
                new_amount = current_amount[0]["amount"] + int(shares)
                # # Set new total amount
                # current_total = db.execute("SELECT total FROM shares WHERE symbol = (?) AND user_id = (?)", symbol, session["user_id"])
                # new_total = format(current_total[0]["total"] + total, ".2f")

                # Update shares amount, price and total
                db.execute("UPDATE shares SET amount = (?), price = (?) WHERE user_id = (?) AND symbol = (?)", new_amount, price, session["user_id"], symbol)
                # Update cash amount
                db.execute("UPDATE users SET cash=(?) WHERE id = (?)", (cash[0]["cash"] - total), session["user_id"])

            else:
                # Add new shares to shares table
                db.execute("INSERT INTO shares (symbol, name, amount, price, user_id) VALUES(?, ?, ?, ?, ?)", symbol, name, shares, price, session["user_id"])

                # Update cash amount
                db.execute("UPDATE users SET cash=(?) WHERE id = (?)", (cash[0]["cash"] - total), session["user_id"])

            return redirect("/")
        else:
            return apology("stock not found")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol");
        data = lookup(symbol)
        if not data:
            return apology("stock not found")
        else:
            return render_template("quoted.html", data = data)
    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure passwords match
        if password != confirmation:
            return apology("passwords didn't match", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username doesn't already exist
        if len(rows) != 0:
            return apology("username already exists", 403)
        else:
            hash = generate_password_hash(password)
            # Insert data into database
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        data = lookup(symbol)
        price = data["price"]
        total = price * float(shares)

        # Check if user has enough shares of the stock
        current_shares = db.execute("SELECT amount FROM shares WHERE symbol= ? AND user_id= ?", symbol, session["user_id"])
        if not current_shares or int(shares) > current_shares[0]["amount"]:
            return apology("not enough shares", 403)
        else:
            # Set new amount of shares
            current_amount = db.execute("SELECT amount FROM shares WHERE symbol = (?) AND user_id = (?)", symbol, session["user_id"])
            new_amount = current_amount[0]["amount"] - int(shares)
            # # Set new total amount
            # current_total = db.execute("SELECT total FROM shares WHERE symbol = (?) AND user_id = (?)", symbol, session["user_id"])
            # new_total = format(current_total[0]["total"] - total, ".2f")

            # Update amount of shares
            db.execute("UPDATE shares SET amount = (?) WHERE user_id = (?) AND symbol = (?)", new_amount, session["user_id"], symbol)

            # Update cash
            cash = db.execute("SELECT cash FROM users WHERE id = (?)", session["user_id"])
            db.execute("UPDATE users SET cash=(?) WHERE id = (?)", (cash[0]["cash"] + total), session["user_id"])

            # Update total of cash
            current_price = db.execute("SELECT price FROM shares WHERE user_id = (?) AND symbol = (?)", session["user_id"], symbol)
            difference = total - (float(current_price[0]["price"])*float(shares))
            current_total = db.execute("SELECT total FROM users WHERE id = (?)", session["user_id"])
            new_total = current_total[0]["total"] + difference
            db.execute("UPDATE users SET total=(?) WHERE id = (?)", new_total, session["user_id"])

        # Redirect user to home page
        return redirect("/")

    else:
        symbols = db.execute("SELECT symbol FROM shares WHERE user_id = ?", session["user_id"])

        return render_template("sell.html", symbols = symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
