from app.models import User, Boat
from flask import session
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
        
def save_boat(user_id, sail_nr, name, type_id):
        """ Adds the boat to the database """

        boat = Boat(user_id=user_id, sail_nr=sail_nr, name=name, type_id=type_id)
        db.session.add(boat)
        db.session.commit()
        print("Boat saved successfully!")