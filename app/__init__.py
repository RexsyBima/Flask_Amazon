from flask import Flask
import os.path
from flask_sqlalchemy import SQLAlchemy
from jinjax import Catalog


DB_NAME = "database.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, DB_NAME)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"

db = SQLAlchemy(app)

catalog = Catalog(jinja_env=app.jinja_env)
catalog.add_folder("app/templates")

from app import routes
