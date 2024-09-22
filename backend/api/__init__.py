# api/__init__.py
from flask import Flask
from flask_cors import CORS
from .models import db
from .models import db


def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Load configuration (optional)
    app.config.from_object('api.config.Config')

    # Initialize extensions
    db.init_app(app)

    # Register blueprints (if any)
    from .routes import main
    app.register_blueprint(main)


    return app
