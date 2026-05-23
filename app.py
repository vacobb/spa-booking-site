from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///spa.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user = db.execute("SELECT * FROM users WHERE user_id = :user_id", user_id=session["user_id"])
    # The 0 here refers to the first item in the list, not a "user_id" of 0
    user = user[0] if user else None

    services = db.execute("""SELECT * FROM services WHERE user_id = :user_id ORDER BY CASE
                        WHEN day = 'Monday' THEN 1
                        WHEN day = 'Tuesday' THEN 2
                        WHEN day = 'Wednesday' THEN 3
                        WHEN day = 'Thursday' THEN 4
                        WHEN day = 'Friday' THEN 5
                        WHEN day = 'Saturday' THEN 6
                        WHEN day = 'Sunday' THEN 7
                        END, time""",
                          user_id=session["user_id"])

    timestamp = datetime.strptime(user['timestamp'], '%Y-%m-%d %H:%M:%S')

    if user:
        user['timestamp'] = timestamp.strftime('%Y')

    if request.method == "GET":
        return render_template("index.html", current_route='index', user=user, services=services)

    else:
        removeservice = request.form.get("removeservice")

        if removeservice is not None:
            user_id = session.get('user_id')
            service_id = request.form.get("service_id")
            db.execute("DELETE FROM services WHERE service_id = ?", service_id)

            return redirect("/")

        else:
            service = request.form.get("service")
            if not service:
                flash("Please select a valid service.")
                return redirect("/")

            day = request.form.get("day")
            if not day:
                flash("Please select a valid day.")
                return redirect("/")

            time = request.form.get("time")
            if not time:
                flash("Please select a valid time.")
                return redirect("/")

            else:
                user_id = session.get('user_id')
                existing_services = db.execute(
                    "SELECT * FROM services WHERE day = :day AND time = :time", day=day, time=time)

                if len(existing_services) == 0:

                    db.execute(
                        "INSERT INTO services (user_id, service, day, time) VALUES(?, ?, ?, ?)", user_id, service, day, time)

                else:
                    flash("Time already booked. Please choose another time.")
                    return redirect("/")

                return redirect("/")


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    user_id = session.get("user_id")

    user = db.execute("SELECT * FROM users WHERE user_id = :user_id", user_id=user_id)
    user = user[0] if user else None

    if user:
        timestamp = datetime.strptime(user['timestamp'], '%Y-%m-%d %H:%M:%S')
        user['timestamp'] = timestamp.strftime('%Y')

    if request.method == "POST":

        if 'update' in request.form:

            firstname = request.form.get("firstname")
            lastname = request.form.get("lastname")

            if not firstname or not lastname:
                flash("Please enter both first and last name.")
                return redirect("/")

            user = session['user_id']
            db.execute("UPDATE users SET firstname = :firstname, lastname = :lastname WHERE user_id = :user_id",
                       firstname=firstname, lastname=lastname, user_id=session['user_id'])

            return redirect("/")

        elif 'uploadPic' in request.form and 'profilePic' in request.files:

            if 'profilePic' not in request.files:
                flash('profilePic not in request.files')
                return redirect("/")

            else:
                profilePic = request.files['profilePic']

                if profilePic.filename == '':
                    flash('No selected file.')
                    return redirect("/")

                filename = profilePic.filename
                file_path = "/workspaces/156117056/final-project/static/profilePics/" + profilePic.filename
                profilePic.save(file_path)
                db.execute("UPDATE users SET profilePic = :filename WHERE user_id = :user_id",
                           filename=filename, user_id=user_id)

            return redirect("/")

    else:

        return render_template("account.html", current_route='account', user=user)

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user id
    session.clear()

    # User reached route via POST
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Please enter username.")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Please enter password.")
            return redirect("/login")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash("Invalid username and/or password.")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect to homepage
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    else:
        firstname = request.form.get("firstname")
        if not firstname:
            flash("Please enter your first name.")
            return redirect("/register")

        lastname = request.form.get("lastname")
        if not lastname:
            flash("Please enter your last name.")
            return redirect("/register")

        username = request.form.get("username")
        if not username:
            flash("Please enter a username.")
            return redirect("/register")
        if db.execute("SELECT * FROM users WHERE username = ?", username):
            flash("Sorry! Username already exists.")
            return redirect("/register")

        password = request.form.get("password")
        if not password:
            flash("Please enter a password.")
            return redirect("/register")

        confirmation = request.form.get("confirmation")
        if confirmation != password:
            flash("Passwords do not match.")
            return redirect("/register")

        hash = generate_password_hash(password)

        db.execute("INSERT INTO users (username, hash, firstname, lastname) VALUES(?, ?, ?, ?)",
                   username, hash, firstname, lastname)
        return redirect("/login")
