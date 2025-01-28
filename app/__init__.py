from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from dotenv import load_dotenv
import os

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    load_dotenv()
    app.secret_key = os.getenv("SECRET_KEY")

    db.init_app(app)
    
    with app.app_context():
        from app import routes, models
        db.create_all()

    return app