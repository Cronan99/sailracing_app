from flask import render_template, request, redirect, url_for, session
from app.models import *
from flask import current_app as app
from app.utils import *


@app.route("/")
def index():
    user = user_auth()
    boat_types = Boat_type.query.all()
    boat_list = Boat.query.all()
    users = User.query.all()
    race_list = Race.query.all()
    return render_template("index.html", boat_types=boat_types, boat_list=boat_list, users=users, user=user, race_list=race_list)
    
    
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
            boat_id = request.form.getlist("boats")
            srs_list = []
            for id in boat_id:
                srs = request.form.get(f"boat_{id}_handicap")
                srs_list.append([id, srs])

            session["race_name"] = race_name
            session["race_date"] = race_date
            session["srs_list"] = srs_list
            session["boat_id"] = boat_id

            return redirect(url_for("race_time"))
            
        boat_types = Boat_type.query.all()
        boat_list = Boat.query.all()
        boat_list.sort(key=lambda boat: boat.name.lower())
        users = User.query.all()

        return render_template("race.html", boat_types=boat_types, boat_list=boat_list, users=users)
    else:
        return redirect(url_for("index"))

@app.route("/racetimes", methods=["GET", "POST"])
def race_time():

    race_name = session.get("race_name")
    race_date = session.get("race_date")
    srs_list = session.get("srs_list")
    boat_id = session.get("boat_id")

    if request.method == "POST":
        times = []
        for id in boat_id:
            hours = request.form.get(f"hours_{id}")
            minutes = request.form.get(f"minutes_{id}")
            seconds = request.form.get(f"seconds_{id}")
            times.append([id, hours, minutes, seconds])
        
        save_race(race_name, race_date, srs_list, times)
        return redirect(url_for("index"))
        

    # Retrieve the boat objects based on IDs
    boats = Boat.query.filter(Boat.id.in_(boat_id)).all()

    return render_template("race_times.html", race_name=race_name, race_date=race_date, srs_list=srs_list, boats=boats)


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
    
@app.route("/leaderboard/<int:race_id>", methods=["GET", "POST"])
def leaderboard(race_id):
    race_stats = Race_stat.query.filter_by(race_id=race_id).all()
    race = Race.query.filter_by(id=race_id).first()
    boat_types = Boat_type.query.all()
    boat_list = []
    user_list = []
    result_list  = []
    for stat in race_stats:
        boat = Boat.query.filter_by(id=stat.boat_id).all()
        boat_list.append(boat)
    for boats in boat_list:
        for boat in boats:
            user = User.query.filter_by(id=boat.user_id).all()
            user_list.append(user)
    for stat in race_stats:
        result_list.append([stat.boat_id, stat.srs_time, stat.time])

    result_list.sort(key=lambda x: x[1])

    return render_template("leaderboard.html",
                            result_list = result_list,
                            boat_list=boat_list,
                            user_list=user_list,
                            race=race,
                            boat_types=boat_types
                            )