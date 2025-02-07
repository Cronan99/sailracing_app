from flask import session, redirect, url_for, flash
from app.models import User, Boat, Race, Race_stat
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import time, datetime


def user_auth():
    """ Checks if there is a user logged in to the session """

    if "user_id" in session:
        user_id = session["user_id"]
        user = User.query.filter_by(id=user_id).first()
        return user
    else:
        return False


def login_check(username, password):

    # Checks that both username and psasword field are filled in
    if not username or not password:
        flash("Username and Password are required!")
        return redirect(url_for("login"))
    
    user = User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password_hash, password):
            
            session["user_id"] = user.id

            return redirect(url_for("index"))
        else:
            flash("Incorrect password!")
            return redirect(url_for("login"))
    else:
        flash("Incorrect username!")

        

def register_user(username, password):
    """ Check the registration and save user to the database """

    # Checks that both username and psasword field are filled in
    if not username or not password:
        flash("Username and Password are required for registration!")
        return redirect(url_for("register"))
    
    # Checks for already existing users with that name
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash("Username is already in use! Please choose another.")
        return redirect(url_for("register"))
    
    if len(password)<=7:
        flash("Password must be atleast 8 characters!")
        return redirect(url_for("register"))

    # Generates hash, creates user object and saves it to the database
    password_hash= generate_password_hash(password)

    user = User(username=username, password_hash=password_hash, admin=False)

    db.session.add(user)
    db.session.commit()

    # After the user is created its redirected to the login page
    flash("Registration is successful! Please login.", "success")
    return redirect(url_for("login"))


def save_boat(user_id, sail_nr, name, type_id):
    """ Adds the boat to the database """

    boat = Boat(user_id=user_id, sail_nr=sail_nr, name=name, type_id=type_id)
    db.session.add(boat)
    db.session.commit()
    print("Boat saved successfully!")


def save_race(race_name, race_date, srs_list, times):

    race_date =  datetime.strptime(race_date, "%Y-%m-%d").date()
    race = Race(name=race_name, date=race_date)
    db.session.add(race)
    db.session.commit()

    for race_time in times:
        for srs in srs_list:
            if race_time[0] == srs[0]:

                race_hours = int(race_time[1]) if race_time[1] else 0
                race_minutes = int(race_time[2]) if race_time[2] else 0
                race_seconds = int(race_time[3]) if race_time[3] else 0
                
                srs_hours, srs_minutes, srs_seconds = calculate_times(race_hours, race_minutes, race_seconds, srs)

                real_time = time(race_hours, race_minutes, race_seconds)
                srs_time = time(srs_hours, srs_minutes, srs_seconds)

                race_stat = Race_stat(race_id=race.id, boat_id=race_time[0], time=real_time, srs_time=srs_time)
                db.session.add(race_stat)
                db.session.commit()

def calculate_times(race_hours, race_minutes, race_seconds, srs):
    total_time_seconds = race_hours * 3600 + race_minutes * 60 + race_seconds
    srs_time_seconds = int(total_time_seconds) * float(srs[1])
    
    srs_hours = int(srs_time_seconds // 3600)
    srs_minutes = int((srs_time_seconds % 3600) // 60)
    srs_seconds = int(srs_time_seconds % 60)

    return (srs_hours, srs_minutes, srs_seconds)