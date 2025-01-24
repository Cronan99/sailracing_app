from flask import render_template, request, redirect, url_for
from app import db
import app.models
from flask import current_app as app


@app.route("/", methods=["GET", "POST"])
def index():
    if True:
        return render_template("index.html")
    else:
        return render_template("login.html")