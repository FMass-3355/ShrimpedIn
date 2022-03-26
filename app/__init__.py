from flask import Flask

# New imports
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from os import environ
import mysql.connector

# force loading of environment variables
load_dotenv('.flaskenv')

# Get the environment variables from .flaskenv
IP = environ.get('MYSQL_IP')
USERNAME = environ.get('MYSQL_USER')
PASSWORD = environ.get('MYSQL_PASS')
DB_NAME = environ.get('MYSQL_DB')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csc33O'

# Specify the connection parameters/credentials for the database
DB_CONFIG_STR = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{IP}/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG_STR
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True


# Create database connection and associate it with the Flask application
db = SQLAlchemy(app)

login = LoginManager(app)

# enables @login_required
login.login_view = 'login'

# Add models
from app import routes, models
from app.models import User

# Create DB schema
db.create_all()

# Create admin and basic user account
user = User.query.filter_by(username='admin').first()
if user is None:
    user_admin = User(username='admin', role='admin')
    user_admin.set_password('csc330sp22')
    db.session.add(user_admin)
    db.session.commit()

user = User.query.filter_by(username='user').first()
if user is None:
    reg_user = User(username='user', role = 'user')
    reg_user.set_password('csc330sp22')
    db.session.add(reg_user)
    db.session.commit()
