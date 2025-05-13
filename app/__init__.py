from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Path to your football.db (adjust if located elsewhere)
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../football.db'))

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register routes
    from app.controllers.routes import main
    app.register_blueprint(main)

    # Import models before creating tables
    from app.models import user, tournament, matches, goal_scorers  # Add goal_scorers here
  # or other models matching football.db schema

    # NOTE: Use db.create_all() ONLY if you're sure it's safe.
    # It won't delete existing tables, but can add missing ones.
    with app.app_context():
        db.create_all()

    return app

