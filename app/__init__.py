from flask import Flask
import os.path
from flask_sqlalchemy import SQLAlchemy
from jinjax import Catalog
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

DB_NAME = "database.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, DB_NAME)
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.secret_key = "a5d697c595e8744ecbfa99df1bfa5df8663e08c4c9ee803c459a90ccc6e7c9cf"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app=app)
catalog = Catalog(jinja_env=app.jinja_env)
catalog.add_folder("app/templates")

from app import routes
