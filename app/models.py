from app import db, login
from flask_login import UserMixin
import requests
from flask import render_template, redirect, url_for, flash, request, session, jsonify, send_file
from io import BytesIO
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import*
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# User extends the flask_login defined UserMixin class.  UserMixin
# provides default functionality that allows us to keep track of
# authenticated user



#===================================================================================================
#Model's Python file is used to create the database stuff
#Please make sure to do db.create_all()
#===================================================================================================

student_application = db.Table('student_application',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('application_id', db.Integer, db.ForeignKey('applications.id'))
)

#===================================================================================================
#user table
#===================================================================================================
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    role = db.Column(db.String(64))
    password_hash = db.Column(db.String(256), unique=True)
    fname = db.Column(db.String(64))
    m_name = db.Column(db.String(64))
    lname = db.Column(db.String(64))

    image_file = db.Column(db.String(20), default='profile.png')
    date_of_birth = db.Column(db.Date)#might not work
    # date_year = db.Column(db.Integer(4))
    # date_month = db.Column(db.String(64))#maybe int for month number
    # date_day = db.Column(db.Integer(2)) 
    phone_number = db.Column(db.Integer)
    address = db.Column(db.String(64))
    zip_code = db.Column(db.Integer) #imad didnt have () so might not work
    city = db.Column(db.String(64))
    state = db.Column(db.String(64)) #want to have a drop down list that can fill in state
    #profile_pic *maybe*
    application = relationship("Application", secondary=student_application)
    company_id = Column(Integer, ForeignKey('companies.id'))
    #resume *maybe*
    #cover_letter *maybe*
    #recomendation(s) ***maybe*** <--might need another table
    #acc_stat = db.Column(db.String(64))
    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on':role
    }
#===================================================================================================
#Password Salting
#===================================================================================================
    def set_password(self, password):
        # Store hashed (encrypted) password in database
        self.password_hash = generate_password_hash(password)
#===================================================================================================
#Password Checking
#===================================================================================================
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
#===================================================================================================



#===================================================================================================
#Job model
#===================================================================================================
class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    #fk student
    #fk recruiter
    #^both user
    #fk company
    job_title = db.Column(db.String(64)) #see how long should be for title and desc.
    job_description = db.Column(db.String(64))
    company = db.Column(db.String(64))
    url = db.Column(db.String(200))
    
    address = db.Column(db.String(64))
    zip_code = db.Column(db.Integer) 
    city = db.Column(db.String(64))
    state = db.Column(db.String(64)) 

    recruiter_id = Column(Integer, ForeignKey('users.id'))
    #resume *maybe*
    #cover_letter *maybe*
    #recomendation(s) ***maybe*** <--might need another table

class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)
    # resume_filename = db.Column(db.String(50))
    # resume_data = db.Column(db.LargeBinary)
    # cl_filename = db.Column(db.String(50))
    # cl_data = db.Column(db.LargeBinary)

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(64)) #see how long should be for title and desc.
    company_description = db.Column(db.String(64))
    #profile_pic *maybe*
    # maybe only one address for either job or company
    # address = db.Column(db.String(64))
    # zip_code = db.Column(db.Integer) 
    # city = db.Column(db.String(64))
    # state = db.Column(db.String(64)) 

    recruiters = relationship("User")

class Student(User):
    __tablename__='student'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'student'}

class Recruiter(User):
    __tablename__='recruiter'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'recruiter'}

class Faculty(User):
    __tablename__='faculty'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'faculty'}

class Admin(User):
    __tablename__='admin'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'admin'}


# API Sprint 3
class JobInfo:
    def __JobInfo__(title, URI, location):
        title = title
        URI = URI
        location = location





#===================================================================================================
# load_user is a function that's used by flask_login to manage the session.
# It simply returns the object associated with the authenticated user.
@login.user_loader
def load_user(id):
    return db.session.query(User).get(int(id))
#===================================================================================================

#===================================================================================================
#Upload files   
#====================================================================================
class Upload(db.Model):
    __tablename__ = 'upload'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    doc_type = db.Column(db.String(64))
    
    
