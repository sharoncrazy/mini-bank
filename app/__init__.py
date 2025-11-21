from flask import Flask, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from Config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Register Blueprints
    from .auth.routes import auth_bp
    from .core.routes import core_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(core_bp)

    # Import models
    from . import models

    # Create tables if not exist (for dev)
    with app.app_context():
        db.create_all()

    return app