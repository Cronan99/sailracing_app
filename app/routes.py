from flask import render_template, request, redirect, url_for
from app.models import *
from flask import current_app as app


@app.route("/", methods=["GET", "POST"])
def index():
    if True:
        boat_types = Boat_type.query.all()

        return render_template("index.html", boat_types=boat_types)
    else:
        return render_template("login.html")