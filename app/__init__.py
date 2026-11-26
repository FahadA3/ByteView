#create_app should build the flask app, load config calls, register blueprints
from app.db import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    db.init_app(app)