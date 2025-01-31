from flask import session, redirect, url_for, flash
from app.models import User, Boat
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


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
    flash("Registration is successful! Please login.")
    return redirect(url_for("login"))
    
        
def save_boat(user_id, sail_nr, name, type_id):
    """ Adds the boat to the database """

    boat = Boat(user_id=user_id, sail_nr=sail_nr, name=name, type_id=type_id)
    db.session.add(boat)
    db.session.commit()
    print("Boat saved successfully!")