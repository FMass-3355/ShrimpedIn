#Imports
#-------From SQLAlchemy---------#
from app import db, login
from sqlalchemy import*
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
#------From Flask Login---------#
from flask_login import UserMixin, current_user
from flask import render_template, redirect, url_for, flash, request, session, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash
#--------Python Library---------#
import requests
from io import BytesIO



# User extends the flask_login defined UserMixin class.  UserMixin
# provides default functionality that allows us to keep track of
# authenticated user

#===================================================================================================
#Model's Python file is used to create the database stuff
#Please make sure to do db.create_all()
#do db.drop_all() to drop all the database
#===================================================================================================


#---------------- Users ----------------#
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    role = db.Column(db.String(32))
    password_hash = db.Column(db.String(256), unique=True)
    fname = db.Column(db.String(64))
    lname = db.Column(db.String(64))
    mname = db.Column(db.String(64))
    address = db.Column(db.String(128))
    city = db.Column(db.String(128))
    zip_code=db.Column(db.String(5))
    state=db.Column(db.String(64))
    date_of_birth = db.Column(db.Date)
    phone_number = db.Column(db.String(128))
    user_bio = db.Column(db.String(512))
    
    #Password Salting
    def set_password(self, password):
        #Store hashed (encrypted) password in database
        self.password_hash = generate_password_hash(password)
    #Password Checking
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)      

    rec_id = relationship("Recruiter", backref="users")
    rec_id2 = relationship("Associations_Application", backref="users")  

#-----Subtype: Recruiter M:N (users:companies)------#
class Recruiter(UserMixin, db.Model):
    __tablename__ = 'recruiter'
    id = db.Column(db.Integer, primary_key=True)
    fk_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fk_company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    fk_rec_id = relationship("Job", backref="recruiter")
#-----Subtype: Recruiter M:N (users:companies)------#
#---------------- Users ----------------#


#------------ Company ----------------#
class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(64), unique=True, nullable=False) #see how long should be for title and desc.
    company_description = db.Column(db.String(1512), default='No company description')
    address = db.Column(db.String(64))
    zip_code = db.Column(db.Integer) 
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    #relates to the recruiter M:N with users
    comp_id=relationship("Recruiter", backref='company')

#------------ Company ----------------#


#------------------Job----------------#
class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    fk_recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiter.id'), nullable=False)
    job_title = db.Column(db.String(64)) #see how long should be for title and desc.
    job_description = db.Column(db.String(1512))
    company = db.Column(db.String(64))
    job_url = db.Column(db.String(256))
    job_address = db.Column(db.String(128))
    job_city = db.Column(db.String(64))
    Job_zip_code = db.Column(db.Integer)

    #Relationship
    job_id=relationship("Associations_Application", backref='jobs')
#------------------Job----------------#



#-----Association table (M:N) 0-----#
#applications
class Associations_Application(db.Model):
   __tablename__ = 'associations_applications'
   id = db.Column(db.Integer, primary_key=True)
   fk_job_id=db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
   fk_user_id= db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
   A_resume=db.Column(db.LargeBinary, nullable=True)
   A_coverletter=db.Column(db.LargeBinary, nullable=True)
#-----Association table (M:N) 0-----#



# API Sprint 3
class JobInfo:
    def __JobInfo__(title, URI, location):
        title = title
        URI = URI
        location = location




#-----------------Upload files----------------------------
class Upload(db.Model):
    __tablename__ = 'upload'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    doc_type = db.Column(db.String(64))
#-----------------Upload files---------------------------- 

#===================================================================================================
# load_user is a function that's used by flask_login to manage the session.
# It simply returns the object associated with the authenticated user.
@login.user_loader
def load_user(id):
    return db.session.query(User).get(int(id))
#===================================================================================================
