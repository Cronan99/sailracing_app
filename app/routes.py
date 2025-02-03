from flask import render_template, request, redirect, url_for, session
from app.models import *
from flask import current_app as app
from app.utils import user_auth, save_boat, login_check, register_user


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

        return login_check(username, password)
                
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Gets username and password from the loginpage and then saves the user to the database."""
    
    if request.method=="POST":

        username = request.form.get("Username")
        password = request.form.get("Password")

        return register_user(username, password)

    return render_template("register.html")


@app.route("/logout")
def logout():
    # Remove the user's id from the session to log them out
    session.pop("user_id", None)

    return redirect(url_for("index"))


@app.route("/race", methods=["GET", "POST"])
def create_race():
    user = user_auth()
    if user.admin:
        if request.method == "POST":
            race_name = request.form.get("raceName")
            race_date = request.form.get("raceDate")
            boats = request.form.getlist("boats")
            srs_list = []
            for boat in boats:
                srs = request.form.get(f"boat_{boat}_handicap")
                srs_list.append(srs)
            print(race_name, race_date, boats, srs_list)


        boat_types = Boat_type.query.all()
        boat_list = Boat.query.all()
        boat_list.sort(key=lambda boat: boat.name.lower())
        users = User.query.all()

        return render_template("race.html", boat_types=boat_types, boat_list=boat_list, users=users)
    else:
        redirect(url_for("index"))


@app.route("/create_boat", methods=["GET", "POST"])
def create_boat():

    if user_auth():
        boat_types = Boat_type.query.all()

        if request.method == "POST":

            user_id = session["user_id"]
            sail_nr = request.form.get("sailnumber")
            boat_name = request.form.get("boat name")
            boat_type = request.form.get("boat")

            save_boat(user_id, sail_nr, boat_name, boat_type)

            return redirect(url_for("index"))
        
        return render_template("create_boat.html", boat_types=boat_types)
    else:
        return redirect(url_for("index"))