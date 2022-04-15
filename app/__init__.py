from ensurepip import bootstrap
from xml.dom.xmlbuilder import DOMEntityResolver
from flask import Flask

# New imports
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from os import environ
import mysql.connector
from flask_moment import Moment
import requests
import sys
from wtforms.validators import DataRequired
import json



# force loading of environment variables
load_dotenv('.flaskenv')

# Get the environment variables from .flaskenv
IP = environ.get('MYSQL_IP')
USERNAME = environ.get('MYSQL_USER')
PASSWORD = environ.get('MYSQL_PASS')
DB_NAME = environ.get('MYSQL_DB')

#API 
# Read values from .flaskenv
API_KEY = environ.get('API_KEY')
API_HOST = environ.get('API_HOST')
API_URL = environ.get('API_URL')
EMAIL = environ.get('EMAIL')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csc33O'
bootstrap = Bootstrap(app)
moment = Moment(app)


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
from app.models import *

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

user = User.query.filter_by(username='recruiter').first()
if user is None:
    rec_user = User(username='recruiter', role = 'recruiter')
    rec_user.set_password('csc330sp22')
    db.session.add(rec_user)
    db.session.commit()





#for sprint 3
user = User.query.filter_by(username='faculty').first()
if user is None:
    fac_user = User(username='faculty', role = 'faculty')
    fac_user.set_password('csc330sp22')
    db.session.add(fac_user)
    db.session.commit()
    

