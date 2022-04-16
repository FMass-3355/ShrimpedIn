import requests
from app import app
from flask import render_template, redirect, url_for, flash, request, session, jsonify, send_file
from io import BytesIO
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import *
from app import db
from app.models import *
import sys
from dotenv import load_dotenv
from os import environ
from wtforms.validators import DataRequired


#===================================================================================================
#API 
# Read values from .flaskenv
#===================================================================================================
API_KEY = environ.get('API_KEY')
API_HOST = environ.get('API_HOST')
API_URL = environ.get('API_URL')
EMAIL = environ.get('EMAIL')
#===================================================================================================

#===================================================================================================
#Homepage
#===================================================================================================
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')
#===================================================================================================


#===================================================================================================
#Logging in is the 
#===================================================================================================
@app.route('/')
def index():
    return redirect(url_for('login'))
#===================================================================================================
#===================================================================================================
#Login Method
#===================================================================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Authenticated users are redirected to home page.
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        # Query DB for user by username
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print('Login failed', file=sys.stderr)
            return redirect(url_for('login'))
        # login_user is a flask_login function that starts a session
        login_user(user)
        print('Login successful', file=sys.stderr)
        return redirect(url_for('homepage'))
    return render_template('login.html', form=form)
#===================================================================================================
#===================================================================================================
#===================================================================================================
#Logging out
#===================================================================================================
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
#===================================================================================================





#===================================================================================================
#Settings
#===================================================================================================
@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')
#===================================================================================================
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if current_user.is_authenticated:
        user = db.session.query(User).filter_by(username=current_user.username).first()
        form = ChangePasswordForm()
    if form.validate_on_submit():
        old_pass = form.old_pass.data
        new_pass = form.new_pass.data
        new_pass_retype = form.new_pass_retype.data
        
        if user.check_password(old_pass):
            print('old password correct', file=sys.stderr)
            if new_pass == new_pass_retype:
                print('password & retype match', file=sys.stderr)
                user.set_password(new_pass)
                db.session.add(user)
                db.session.commit()
            else:
                print('password & retype do not match', file=sys.stderr)
        else:
            print('old password incorrect', file=sys.stderr)
        return redirect(url_for('index'))
    '''
    Implement this function for Activity 9.
    Verify that old password matches and the new password and retype also match.
    '''
    return render_template('change_password.html', form = form)
#===================================================================================================




#===================================================================================================
#Add user
#===================================================================================================
'''
Use by the admin to create new users
'''
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if is_admin():
        form = CreateUserForm()
        if form.validate_on_submit():
            fname = form.fname.data
            lname = form.lname.data
            username = form.username.data
            password = form.password.data
            email = form.email.data
            if not db.session.query(User).filter_by(email=email).first():
                user = User(username=username, email=email, role='user', fname=fname, lname=lname)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
        all_usernames= db.session.query(User.username).all()
        print(all_usernames, file=sys.stderr)
        return render_template('add_user.html', form=form)
    return render_template('invalid_credentials.html')
#===================================================================================================
#===================================================================================================
#Create User
#===================================================================================================
@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
        form = CreateUserForm()
        if form.validate_on_submit():
            fname = form.fname.data
            lname = form.lname.data
            username = form.username.data
            password = form.password.data
            email = form.email.data
            if not db.session.query(User).filter_by(email=email).first():
                user = User(username=username, email=email, role='user', fname=fname, lname=lname)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
        all_usernames= db.session.query(User.username).all()
        print(all_usernames, file=sys.stderr)
        return render_template('create_user.html', form=form)
#===================================================================================================
#===================================================================================================
#Profile creation
#===================================================================================================
@app.route('/profile')
@login_required
def profile():
    if current_user.is_authenticated:
        username = current_user.username
        fname = current_user.fname
        lname = current_user.lname
        email = current_user.email
        print(fname, file=sys.stderr)
    
    return render_template('profile.html', fname=fname, lname=lname, email=email, username=username)
#===================================================================================================

#===================================================================================================
#uploading and downloading files 
#===================================================================================================
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']

        upload = Upload(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()

        return f'Uploaded: {file.filename}'
    return render_template('index.html')


@app.route('/download/<upload_id>')
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data), attachment_filename=upload.filename, as_attachment=True)
        
#===================================================================================================




#===================================================================================================
#Job adding Functionality
#===================================================================================================
@app.route('/jobs')
@login_required
def jobs():
    if current_user.is_authenticated:
        title = db.session.query(Job).filter
    return render_template('jobs.html', job_title=title)
#===================================================================================================







#===================================================================================================
#Messaging/Chat
#===================================================================================================
@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')
#===================================================================================================
@app.route('/account_recovery', methods=['GET', 'POST'])
def recover_account():
    form = AccountRecovery()
    if form.validate_on_submit():
        username = form.username.data
        if db.session.query(User).filter_by(username=username).first():
            print("Account Recovered")
    return render_template('account_recovery.html', form=form)





#JOB SECTION
#===================================================================================================
#CREATE JOB
#===================================================================================================
@app.route('/create_job', methods=['GET', 'POST'])
@login_required
def add_job():
    if is_recruiter() or is_student() or is_admin():
        form = AddJob()
        if form.validate_on_submit():
            job_title = form.job_title.data
            company = form.company.data
            description = form.job_description.data
            url = form.url.data
            job_posting = Job(job_title=job_title, company=company, job_description=description, url=url)
            db.session.add(job_posting)
            db.session.commit()
            #all_jobs= db.session.query(Job.job_title).all()
            #print(all_jobs, file=sys.stderr)
        return render_template('create_jobs.html', form=form)
    return render_template('invalid_credentials.html')
#===================================================================================================

#===================================================================================================
#API INFORMATION
#===================================================================================================

#API / SEARCH (API is on top of the file)
@app.route('/search', methods=['GET', 'POST'])
def search():
    headers =   {'Host': API_HOST,
                'User-Agent': EMAIL,
                'Authorization-Key': API_KEY}
    form = SearchForm()
    if form.validate_on_submit():
        city = form.city.data + '%20' + form.state.data
        keyword = form.keyword.data
        full_URL = f'{API_URL}?LocationName={city}&Keyword={keyword}&ResultsPerPage=50'
        response = requests.get(full_URL, headers = headers)

        if response.status_code == 200:
            print('Success!', file = sys.stdout)
        elif response.status_code == 404:
            print('Not found.', file=sys.stdout)

         # Extract title, location and URI from API and package as a list of
         # objects (job_results)
        response_json = response.json()
        job_results = []
        for item in response_json['SearchResult']['SearchResultItems']:
            job = JobInfo()
            job.URI = item['MatchedObjectDescriptor']['PositionURI']
            job.title = item['MatchedObjectDescriptor']['PositionTitle']
            job.location = item['MatchedObjectDescriptor']['PositionLocationDisplay']
            job_results.append(job)

         # display search results as an HTML table
        return render_template('view_jobs.html', job_results=job_results)
    else:
        return render_template('search.html', form=form)
#===================================================================================================



#===================================================================================================
#ERRORS
#===================================================================================================
#@app.errorhandler('/error505')
#def error505():
    r#eturn render_template("505error.html")
#===================================================================================================


#STANDALONE FUNCTION SECTION
###################################################################
def is_admin():
    '''
    Helper function to determine if authenticated user is an admin.
    '''
    if current_user:
        if current_user.role == 'admin':
            return True
        else:
            return False
    else:
        print('User not authenticated.', file=sys.stderr)

def is_recruiter():
    '''
    Helper function to determine if authenticated user is a recruiter.
    '''
    if current_user:
        if current_user.role == 'recruiter':
            return True
        else:
            return False
    else:
        print('User not authenticated.', file=sys.stderr)

def is_student():
    '''
    Helper function to determine if authenticated user is a student.
    '''
    if current_user:
        if current_user.role == 'student':
            return True
        else:
            return False
    else:
        print('User not authenticated.', file=sys.stderr)

def is_faculty():
    '''
    Helper function to determine if authenticated user is a faculty.
    '''
    if current_user:
        if current_user.role == 'faculty':
            return True
        else:
            return False
    else:
        print('User not authenticated.', file=sys.stderr)








