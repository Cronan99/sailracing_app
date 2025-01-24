from app import db
from sqlalchemy import ForeignKey


class User(db.Model):
    """ User class contain id name and password aswell as a boolean if the user in admin or not """
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

class Boat(db.Model):
    """ Boat class is the boat object that is in a relation to a user """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String(255), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey("boat_type.id"))

class Boat_type(db.Model):
    """ Boat_type contains data from the web with handicap and type name """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    srs = db.Column(db.Float, nullable=False)
    srs_ns = db.Column(db.Float, nullable=False) #no spin   
    srs_sh = db.Column(db.Float, nullable=False) #shorthanded
    srs_sh_ns = db.Column(db.Float, nullable=False) #shorthanden no spin

class Race(db.Model):
    """ Race contains id name and race date """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)

class Race_stat(db.Model):
    """ Race_stat contains statistics from races in relation to a boat and a race to show its specific time """

    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, ForeignKey("race.id"))
    boat_id = db.Column(db.Integer, ForeignKey("boat.id"))
    time = db.Column(db.Time)
    srs_time = db.Column(db.Time)