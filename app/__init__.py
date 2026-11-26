from app.db import db
import os
from dotenv import load_dotenv
from flask import Flask

def create_app():
    load_dotenv()
    app = Flask(__name__)

    db_url = os.environ['DATABASE_URL']
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True}

    db.init_app(app)

    from app import models
    from app.routes import register_blueprints
    register_blueprints(app)

    return app