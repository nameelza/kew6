import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

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

    # Count total (cash + total shares amount)
    shares_totals = db.execute("SELECT total FROM shares WHERE user_id = ?", session["user_id"])
    shares_totals_sum = 0
    for key in shares_totals:
        shares_totals_sum += key["total"]
    total_cash = cash[0]['cash'] + shares_totals_sum


    data = db.execute("SELECT * FROM shares WHERE user_id = ?", session["user_id"])

    return render_template("index.html", cash=cash[0]['cash'], total=total_cash, data=data)


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
                # Set new total amount
                new_total = new_amount*price

                # Update shares amount, price and total
                db.execute("UPDATE shares SET amount = ?, price = ?, total = ? WHERE user_id = ? AND symbol = ?", new_amount, price, new_total, session["user_id"], symbol)
                # Update cash amount
                db.execute("UPDATE users SET cash=(?) WHERE id = (?)", (cash[0]["cash"] - total), session["user_id"])

            else:
                # Add new shares to shares table
                db.execute("INSERT INTO shares (symbol, name, amount, price, total, user_id) VALUES(?, ?, ?, ?, ?, ?)", symbol, name, shares, price, total, session["user_id"])

                # Update cash amount
                db.execute("UPDATE users SET cash=(?) WHERE id = (?)", (cash[0]["cash"] - total), session["user_id"])

            # Insert data into history table
            curr_time = datetime.now()
            dt_string = curr_time.strftime("%Y-%m-%d %H:%M:%S")
            db.execute("INSERT INTO history (symbol, shares, price, time, user_id) VALUES(?, ?, ?, ?, ?)", symbol, shares, price, dt_string, session["user_id"])


            cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

            # Count total (cash + total shares amount)
            shares_totals = db.execute("SELECT total FROM shares WHERE user_id = ?", session["user_id"])
            shares_totals_sum = 0
            for key in shares_totals:
                shares_totals_sum += key["total"]
            total_cash = cash[0]['cash'] + shares_totals_sum


            data = db.execute("SELECT * FROM shares WHERE user_id = ?", session["user_id"])

            return render_template("index.html", cash=cash[0]['cash'], total=total_cash, data=data, is_bought=True)

        else:
            return apology("stock not found")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    data = db.execute("SELECT * FROM history WHERE user_id = ?", session["user_id"])

    return render_template("history.html", data = data)


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

@app.route("/account")
@login_required
def account():
    """View account page"""

    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    return render_template("account.html", username = username[0]["username"], cash = cash[0]["cash"])


@app.route("/reset_password", methods=["POST"])
def reset_password():
    """Change password"""

    curr_password = request.form.get("old password")
    new_password = request.form.get("new password")

    # Query database for hash
    hash = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])

    # Check if old password is right
    if not check_password_hash(hash[0]["hash"], curr_password):
        return apology("your current password is not valid", 403)
    # Change password
    else:
        new_hash = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hash, session["user_id"])

    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    return render_template("account.html", username = username[0]["username"], cash = cash[0]["cash"], password_is_changed=True)

@app.route("/add_cash", methods=["POST"])
def add_cash():
    """Add cash"""

    cash_add = request.form.get("added cash")

    current_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    new_cash = current_cash[0]["cash"] + float(cash_add)
    db.execute("UPDATE users SET cash = ?", new_cash)

    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    return render_template("account.html", username = username[0]["username"], cash=new_cash, cash_is_added=True)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        input = request.form.get("symbol")
        shares = request.form.get("shares")

        data = lookup(input)
        symbol = data["symbol"]
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
            # Set new total amount*price
            total_shares = new_amount*price
            # Update amount of shares, total amount*price and new price
            db.execute("UPDATE shares SET amount = ?, total = ?, price = ? WHERE user_id = (?) AND symbol = (?)", new_amount, total_shares, price, session["user_id"], symbol)

            # Update cash
            cash = db.execute("SELECT cash FROM users WHERE id = (?)", session["user_id"])
            db.execute("UPDATE users SET cash=(?) WHERE id = (?)", (cash[0]["cash"] + total), session["user_id"])

            # Insert data into history table
            curr_time = datetime.now()
            dt_string = curr_time.strftime("%Y-%m-%d %H:%M:%S")
            sold_shares = 0 - int(shares)
            db.execute("INSERT INTO history (symbol, shares, price, time, user_id) VALUES(?, ?, ?, ?, ?)", symbol, sold_shares, price, dt_string, session["user_id"])

            if current_shares[0]["amount"] == int(shares):
                db.execute("DELETE FROM shares WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)


            # Redirect user to home page
            cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

            # Count total (cash + total shares amount)
            shares_totals = db.execute("SELECT total FROM shares WHERE user_id = ?", session["user_id"])
            shares_totals_sum = 0
            for key in shares_totals:
                shares_totals_sum += key["total"]
            total_cash = cash[0]['cash'] + shares_totals_sum


            data = db.execute("SELECT * FROM shares WHERE user_id = ?", session["user_id"])

            return render_template("index.html", cash=cash[0]['cash'], total=total_cash, data=data, is_sold=True)

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
