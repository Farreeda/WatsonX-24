# init_db.py
from api import create_app
from api.models import db

app = create_app()

with app.app_context():
    db.create_all()
