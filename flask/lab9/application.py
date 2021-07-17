import os

import cs50
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        # access data from form
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        # insert data into database
        db.execute("INSERT INTO bdays (name, month, day) VALUES(?, ?, ?)", name, month, day)

        # go back to homepage
        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        bdays = db.execute("SELECT * FROM bdays")
        return render_template("index.html", bdays=bdays)


