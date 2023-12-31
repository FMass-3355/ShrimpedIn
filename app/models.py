#Imports
#-------From SQLAlchemy---------#
from email.policy import default
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
    image_file = db.Column(db.String(20), default='profile.png')
    
    #Password Salting
    def set_password(self, password):
        #Store hashed (encrypted) password in database
        self.password_hash = generate_password_hash(password)
    #Password Checking
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)      

    rec_id = relationship("Recruiter", cascade='all,delete', backref="users")
    rec_id2 = relationship("Associations_Application", cascade='all,delete', backref="users")  

#-----Subtype: Recruiter M:N (users:companies)------#
class Recruiter(UserMixin, db.Model):
    __tablename__ = 'recruiter'
    id = db.Column(db.Integer, primary_key=True)
    fk_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fk_company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    fk_rec_id = relationship("Job", cascade='all,delete', backref="recruiter")
#-----Subtype: Recruiter M:N (users:companies)------#
#---------------- Users ----------------#


#------------ Company ----------------#
class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(64), unique=True, nullable=False) #see how long should be for title and desc.
    company_description = db.Column(db.String(1512), default='No company description')
    address = db.Column(db.String(64))
    zip_code = db.Column(db.String(5)) 
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
    job_salary = db.Column(db.String(32), default="Negotiable")
    job_url = db.Column(db.String(256))
    job_address = db.Column(db.String(128), default="TBD",nullable=True)
    job_city = db.Column(db.String(64), default="TBD", nullable=True)
    job_state = db.Column(db.String(2), default="TBD", nullable=True)
    job_zipcode = db.Column(db.String(5), default="TBD",nullable=True)

    #Relationship
    job_id=relationship("Associations_Application", cascade='all,delete', backref='jobs')
#------------------Job----------------#

# class Education(db.Model):
#     __tablename__ = 'education'
#     id = db.Column(db.Integer, primary_key=True)

#     user_id = Column(Integer, ForeignKey('users.id'))

# class Experience(db.Model):
#     __tablename__ = 'experience'
#     id = db.Column(db.Integer, primary_key=True)

#     user_id = Column(Integer, ForeignKey('users.id'))

# class Skill(db.Model):
#     __tablename__ = 'skill'
#     id = db.Column(db.Integer, primary_key=True)

#     user_id = Column(Integer, ForeignKey('users.id'))




#-----Association table (M:N) 0-----#
#applications
class Associations_Application(db.Model):
   __tablename__ = 'associations_applications'
   id = db.Column(db.Integer, primary_key=True)
   fk_job_id=db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False) #MAKE FALSE AFTER TESTING
   fk_user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
   status = db.Column(db.String(64), default="Pending")
#    job_id=relationship('',cascade='')
   A_resume=db.Column(db.Integer, db.ForeignKey('upload.id'), nullable=True)
   A_coverletter=db.Column(db.LargeBinary, nullable=True)
   


#-----Association table (M:N) 0-----#

class UserInfo:
    def __UserInfo__(user_id,username,email,role):
        user_id = user_id
        username = username
        email = email
        role = role

# API Sprint 3
#NOT PART OF DATABASE MODEL
#add recruiter id?
class JobInfo:
    def __JobInfo__(job_id, title, URI, location):
        job_id = job_id
        title = title
        URI = URI
        location = location

class JobInfo2:
    def __JobInfo2__(job_id, title, company, Salary, location_address,location_city, location_state, location_zipcode):
        job_id = job_id
        title = title
        company=company
        Salary = Salary
        location_address = location_address
        location_city = location_city
        location_zipcode = location_zipcode
        location_state = location_state
    

class Applicants:
    def __applicants__(user_id, username, email, status):
        user_id = user_id
        username = username
        email = email
        status = status

class Applicants2:
    def __applicants2__(job_id, title, company ,status):
        job_id = job_id
        title = title
        company = company
        status = status


#-----------------Upload files----------------------------
class Upload(db.Model):
    __tablename__ = 'upload'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    doc_type = db.Column(db.String(64))
    user_id = Column(Integer, ForeignKey('users.id'))
    
    upload_applicationlink = relationship("Associations_Application", cascade='save-update', backref="upload")
#-----------------Upload files---------------------------- 

#-----------------Jobs stats--------------------------
#class NationalJobs(db.Model):
   # __tablename__ = 'nationaljobs'
    #id = db.Column(db.Integer, primary_key=True)
    #careers = db.Column(db.String(255))
    #employment_rise = db.Column(db.String(64))
    #average_mean = db.Column(db.String(64))
    #mean_rise = db.Column(db.String(64))

    #Hourly Percentile
    #-------------------------------------------
   # hourly_10th_perc = db.Column(db.String(64))
   # hourly_25th_perc = db.Column(db.String(64))
   # hourly_med_perc = db.Column(db.String(64))
   # hourly_75th_perc = db.Column(db.String(64))
   # hourly_90th_perc = db.Column(db.String(64)) 
    #-------------------------------------------

    #annual Percentile

   # average_10th_perc = db.Column(db.String(64))
   # average_25th_perc = db.Column(db.String(64))
   # average_med_perc = db.Column(db.String(64))
    #average_75th_perc = db.Column(db.String(64))
    #average_90th_percentile = db.Column(db.String(64))
#-----------------Jobs stats--------------------------




#===================================================================================================
# load_user is a function that's used by flask_login to manage the session.
# It simply returns the object associated with the authenticated user.
@login.user_loader
def load_user(id):
    return db.session.query(User).get(int(id))
#===================================================================================================


