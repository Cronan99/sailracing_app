from app import db
from sqlalchemy import ForeignKey


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

class Boat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String(255), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey("boat_type.id"))

class Boat_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    srs = db.Column(db.Float, nullable=False)
    srs_ns = db.Column(db.Float, nullable=False)
    srs_sh = db.Column(db.Float, nullable=False)
    srs_sh_ns = db.Column(db.Float, nullable=False)

class Race(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)

class Race_stat(db.Model):
    race_id = db.Column(db.Integer, ForeignKey("race.id"))
    boat_id = db.Column(db.Integer, ForeignKey("boat.id"))
    time = db.Column(db.Time)
    srs_time = db.Column(db.Time)