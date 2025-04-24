from flask import Flask
from .extentions import db, migrate
from .models import user, product, cart, transaction, review


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    db.init_app(app)
    migrate.init_app(app, db)

    return app