from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import *
from flask import current_app as app
from app.utils import user_auth, save_boat


@app.route("/")
def index():
    user = user_auth()
    boat_types = Boat_type.query.all()
    boat_list = Boat.query.all()
    users = User.query.all()
    return render_template("index.html", boat_types=boat_types, boat_list=boat_list, users=users, user=user)
    
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method=="POST":
        username = request.form.get("Username")
        password = request.form.get("Password")

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password_hash, password):
                
                session["user_id"] = user.id

                return redirect(url_for("index"))
                
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Gets username and password from the loginpage and then saves the user to the database."""
    
    if request.method=="POST":

        username = request.form.get("Username")
        password = request.form.get("Password")

        # Checks that both username and psasword field are filled in
        if not username or not password:
            flash("Username and Password are required for registration!")
            return redirect(url_for("register"))
        
        # Checks for already existing users with that name
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username is already in use! Please choose another.")
            return redirect(url_for("register"))
        
        # Generates hash, creates user object and saves it to the database
        password_hash= generate_password_hash(password)

        user = User(username=username, password_hash=password_hash, admin=False)

        db.session.add(user)
        db.session.commit()

        # After the user is created its redirected to the login page
        flash("Registration is successful! Please login.")
        return redirect(url_for("login"))
    
    return render_template("register.html")


@app.route("/logout")
def logout():
    # Remove the user's id from the session to log them out
    session.pop("user_id", None)

    return redirect(url_for("index"))

@app.route("/race")
def create_race():
    user = user_auth()
    if user.admin:
        return render_template("race.html")
    else:
        redirect(url_for("index"))

@app.route("/create_boat", methods=["GET", "POST"])
def create_boat():
    boat_types = Boat_type.query.all()
    if request.method == "POST":
        user_id = session["user_id"]
        sail_nr = request.form.get("sailnumber")
        boat_name = request.form.get("boat name")
        boat_type = request.form.get("boat")
        save_boat(user_id, sail_nr, boat_name, boat_type)
        return redirect(url_for("index"))
    return render_template("create_boat.html", boat_types=boat_types)