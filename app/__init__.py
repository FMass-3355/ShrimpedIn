#===================================================================================================
from flask import Flask
#===================================================================================================
# New imports
#===================================================================================================
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from os import environ
import mysql.connector
import requests
import sys
from wtforms.validators import DataRequired
import json
#===================================================================================================





#===================================================================================================
# force loading of environment variables
load_dotenv('.flaskenv')
#===================================================================================================
#===================================================================================================
# Get the environment variables from .flaskenv
IP = environ.get('MYSQL_IP')
USERNAME = environ.get('MYSQL_USER')
PASSWORD = environ.get('MYSQL_PASS')
DB_NAME = environ.get('MYSQL_DB')
#===================================================================================================
#===================================================================================================
#API
#=================================================================================================== 
# Read values from .flaskenv
API_KEY = environ.get('API_KEY')
API_HOST = environ.get('API_HOST')
API_URL = environ.get('API_URL')
EMAIL = environ.get('EMAIL')
#===================================================================================================
#===================================================================================================
#APP initialization stuff
#===================================================================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'csc33O'
bootstrap = Bootstrap(app)
app.static_folder = "static"
#===================================================================================================
#===================================================================================================
# Specify the connection parameters/credentials for the database
#===================================================================================================
DB_CONFIG_STR = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{IP}/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG_STR
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True
#===================================================================================================
#===================================================================================================
# Create database connection and associate it with the Flask application
db = SQLAlchemy(app)
login = LoginManager(app)
#===================================================================================================









#===================================================================================================
# enables @login_required
login.login_view = 'login'
#===================================================================================================

#===================================================================================================
# Add models
#===================================================================================================
from app import routes, models
from app.models import *


#Drop Database to refresh (Comment out later once statisfied)
#db.drop_all()
db.create_all()




    


#--------- Sample Users for the database ---------------#
#-------------Test users--------------------------------#
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

user = User.query.filter_by(username='student').first()
if user is None:
    rec_user = User(username='student', role = 'student')
    rec_user.set_password('csc330sp22')
    db.session.add(rec_user)
    db.session.commit()

user = User.query.filter_by(username='faculty').first()
if user is None:
    fac_user = User(username='faculty', role = 'faculty')
    fac_user.set_password('csc330sp22')
    db.session.add(fac_user)
    db.session.commit()
#-------------Test users-------------------------------#


#------------------More Detailed Users -----------------#
user=User.query.filter_by(username='MarcusP11').first()
if user is None:
    custom_user = User(username='MarcusP11', email='MarP1999@southernct.edu', role='student', fname='Marcus', lname='Peterson', date_of_birth='1999-02-02', user_bio="""
    Up comming Graduate student of 2025, Major: Mechanical Engineering, Minor: Mathematics. Looking for Mechanical Engineering related jobs. I have skills in CAD drawings,
    assisted in construction management.""")
    custom_user.set_password('123')
    db.session.add(custom_user)
    db.session.commit()

user=User.query.filter_by(username='EmilJohn23').first()
if user is None:
    custom_user = User(username='EmilJohn23', email='EmilyJohonson02@southernct.edu', role='student', fname='Emily', lname='Johnson', date_of_birth='1999-02-02', user_bio="""
    Senior at SSCSU, Bachelors in business and finance.""")
    custom_user.set_password('123')
    db.session.add(custom_user)
    db.session.commit()

user=User.query.filter_by(username='IAntonio05').first()
if user is None:
    custom_user = User(username='IAntonio05', email='Iantonio05@southernct.edu', role='professor', fname='Ian', lname='Antonio', date_of_birth='1988-02-02', user_bio="""
    Ph.D in Aerospace engineering. Masters in Bio-engineering. AI Developer at Google. IEEE board member. Professor at SCSU.""")
    custom_user.set_password('123')
    db.session.add(custom_user)
    db.session.commit()

user=db.session.query(User).filter_by(username='ArtMar23').first()
if user is None:
    custom_user = User(username='ArtMar23', email='artmar80@gmail.com', role='recruiter', fname='Arthur', lname='Martinez', date_of_birth='1999-02-02')
    custom_user.set_password('123')
    db.session.add(custom_user)
    db.session.commit()

user=User.query.filter_by(username='FrankyMaz').first()
if user is None:
    custom_user = User(username='FrankyMaz', email='FraMaz45@hotmail.com', role='regular', fname='Franky', lname='Mazes', date_of_birth='1999-02-02')
    custom_user.set_password('123')
    db.session.add(custom_user)
    db.session.commit()
#------------------More Detailed Users -----------------#


#---------------------Companies--------------------------#
company = Company.query.filter_by(company_name='Rockeye Technologies').first()
if company is None:
    company = Company(company_name='Rockeye Technologies', address='513 Iron industrial road', zip_code='06142', city='Metropolis', state='New York')
    db.session.add(company)
    db.session.commit()

company = Company.query.filter_by(company_name='Red Shift Bio-Labs').first()
if company is None:
    company = Company(company_name='Red Shift Bio-Labs', address='54 Alison Bacterium', zip_code='07321', city='Gotham', state='New York')
    db.session.add(company)
    db.session.commit()

company = Company.query.filter_by(company_name='Genuidine Business Corp.').first()
if company is None:
    company = Company(company_name='Genuidine Business Corp.', address='370 Eager Street', zip_code='11321', city='New York', state='New York')
    db.session.add(company)
    db.session.commit()
#---------------------Companies--------------------------#


user=User.query.filter_by(username='ArtMar23', role='recruiter').first()
company = Company.query.filter_by(company_name='Rockeye Technologies').first()
if (user is not None and company is not None) and Recruiter.query.filter_by(fk_user_id=user.id, fk_company_id=company.id).first() is None:
    recruiter_Add=Recruiter(fk_user_id=user.id, fk_company_id=company.id)
    db.session.add(recruiter_Add)
    db.session.commit()

