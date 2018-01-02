from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

import os
import re

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///urhome.db")

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
    """Show landing page"""
    return render_template("index.html")


@app.route("/map")
def map_show():
    """Load map of resources"""
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return render_template("map.html", key=os.environ.get("API_KEY"))


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    """Log resource provider in"""

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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        resource_names = db.execute("SELECT Name FROM resources")
        return render_template("custom.html", resources = resource_names)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sign_in.html")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    """Allow resource provider to create account"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        #ensure password is same as password confirmation
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("password and confirmation must match", 400)

        hash = generate_password_hash(request.form.get("password"))

        #Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                         username=request.form.get("username"))

        # Ensure username is unique
        if len(rows) != 0:
           return apology("username taken", 403)

        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash= hash)
        if not result:
            return apology("Username taken", 400)

        # Remember which user has logged in
        session["user_id"] = result

        # Redirect user to home page
        resource_names = db.execute("SELECT Name FROM resources")
        return render_template("custom.html", resources = resource_names)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sign_up.html")


@app.route("/custom", methods=["GET", "POST"])
def custom():
    """Allow resource provider to create account"""

    if request.method == "POST":

        # Ensure additional details are text and are properly submitted
        if not request.form.get("comment"):
            return apology("must provide comment", 400)

        else:
            db.execute("UPDATE resources SET Extra = :Extra WHERE Name = :Name", Extra = request.form.get("comment"), Name = request.form.get("resource_name"))
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("custom.html")


@app.route("/logout")
def logout():
    """Log resource provider out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/search")
def search():
    """Map function that searches for places that match query specified by user"""
    q = request.args.get("q") + "%"

    # Create functionality for zip code searches
    searches = db.execute("SELECT * FROM places WHERE postal_code LIKE :q OR place_name LIKE :q OR admin_name1 LIKE :q OR place_name + ',' + admin_name1 LIKE :q", q=q)
    return jsonify(searches)


@app.route("/update")
def update():
    """Map function that finds all resources within view"""

    # Ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # Ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # Explode southwest corner into two variables
    sw_lat, sw_lng = map(float, request.args.get("sw").split(","))

    # Explode northeast corner into two variables
    ne_lat, ne_lng = map(float, request.args.get("ne").split(","))

    # Find resources within view, pseudorandomly chosen if more within view
    if sw_lng <= ne_lng:

        # Doesn't cross the antimeridian
        rows = db.execute("""SELECT * FROM resources
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
                          ORDER BY RANDOM()
                          """,
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # Crosses the antimeridian
        rows = db.execute("""SELECT * FROM resources
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
                          ORDER BY RANDOM()
                          """,
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # Output resources as JSON
    return jsonify(rows)
