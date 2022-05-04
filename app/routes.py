#Imports
from app import app
#-------environment-------#
from dotenv import load_dotenv
from os import environ
#------SQLAlchemy---------#
from app import db
from app.models import *
#------flask------#
from flask import render_template, redirect, url_for, flash, send_file, flash
from flask_login import login_user, logout_user, login_required, current_user
#------WTFForms---------#
from app.forms import *
from wtforms.validators import DataRequired
#--------Externals-----#
import sys
import requests
from io import BytesIO

from flask_wtf.file import FileField


#API (needed for the USAjobs stuff and other APIs)
API_KEY = environ.get('API_KEY')
API_HOST = environ.get('API_HOST')
API_URL = environ.get('API_URL')
EMAIL = environ.get('EMAIL')






#------------------------------------------------------------ Static Webpages ----------------------------------------------------------------#
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')
  
  
@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')
#------------------------------------------------------------ Static Webpages ----------------------------------------------------------------#



#------------------------------------------------------------- Logging in and Out-----------------------------------------------#
#Start with here
@app.route('/')
def index():
    return redirect(url_for('login'))
    
#Login Method
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

#Logging out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
#------------------------------------------------------------- Logging in and Out-----------------------------------------------#




#------------------------------------------------------------- Account Methods ----------------------------------------------------------------#
#Profile Settings
@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

#Change Password
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
  
  
#Create user (User Method)
@app.route('/create_user', methods=['GET', 'POST'])
def create_user(): 
    form = CreateUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        role = form.role.data
        fname = form.fname.data
        lname = form.lname.data
        mname = form.mname.data
        dob = form.date_of_birth.data
        
        if not db.session.query(User).filter_by(email=email).first():
            user = User(username=username, email=email, role=role, fname=fname,
                        lname=lname, mname=mname, date_of_birth=dob)
            print(user, file=sys.stderr)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
        return redirect(url_for('login'))
    all_usernames= db.session.query(User.username).all()
    print(all_usernames, file=sys.stderr)
    return render_template('create_user.html', form=form)

#------------------------------------------------------------- Account Methods ----------------------------------------------------------------#




#----------------------------------------------------------- Administrator Methods ------------------------------------------------------------#
#Admin adds an user to the database
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
#----------------------------------------------------------- Administrator Methods ------------------------------------------------------------#



#---------------------------------------------------------- Profiles --------------------------------------------------------------------------#
#Profile
@app.route('/profile/')
@login_required
def profile():
    if current_user.is_authenticated:
        username = current_user.username
        fname = current_user.fname
        lname = current_user.lname
        email = current_user.email
        mname = current_user.mname

        dob = current_user.date_of_birth

        address = current_user.address
        city = current_user.city
        state = current_user.state
        zip_code = current_user.zip_code
        phone_number = current_user.phone_number
        user_bio = current_user.user_bio
        # image_file = url_for('static', filename='images/' + current_user.image_file)
        exists = db.session.query(Upload.id).filter_by(user_id=current_user.id, doc_type="profile_pic").first()
        if exists:
            image_file = db.session.query(Upload).filter_by(user_id=current_user.id, doc_type="profile_pic").with_entities(Upload.data).first()
        else:
            image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('profile.html', fname=fname, lname=lname, email=email, username=username, 
                            mname=mname, date_of_birth=dob, address=address, city=city, state=state,
                            zip_code=zip_code, phone_number=phone_number, user_bio=user_bio, image_file=image_file)
    #image_file=image_file

@app.route('/account_recovery', methods=['GET', 'POST'])
def recover_account():
    form = AccountRecovery()
    if form.validate_on_submit():
        username = form.username.data
    if db.session.query(User).filter_by(username=username).first():
        print("Account Recovered")
        return render_template('account_recovery.html', form=form)
    
    
#Edit
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        #---------------------------# 
        address = form.address.data
        city = form.city.data
        state = form.state.data
        zip_code = form.zip_code.data
        #---------------------------# 
        phone_number = form.phone_number.data
        fname = form.fname.data
        mname = form.mname.data
        lname = form.lname.data
        user_bio = form.user_bio.data
        #---------------------------# 
        if fname == '':
            current_user.fname = current_user.fname
        else:
            current_user.fname = fname
            
        if mname == '':
            current_user.mname = current_user.mname
        else:
            current_user.mname = mname

        if lname == '':
            current_user.lname = current_user.lname
        else:
            current_user.lname = lname

        if zip_code == '':
            current_user.zip_code = current_user.zip_code
        else:
            current_user.zip_code = zip_code

        if phone_number == '':
            current_user.phone_number = current_user.phone_number
        else:
            current_user.phone_number = phone_number

        if user_bio == '':
            current_user.user_bio = current_user.user_bio
        else:
            current_user.user_bio = user_bio

       

        if state == '':
            current_user.state = current_user.state
        else:
            current_user.state = state

        if city == '':
            current_user.city = current_user.city       
        else:
            current_user.city = city

        if address == '':
            current_user.address = current_user.address
        else:
            current_user.address = address

        db.session.add(current_user)
        db.session.commit()

        return redirect(url_for('profile'))
    image_file = url_for('static', filename='images/' + 'profile.png')
    return render_template('edit_profile.html', form=form, image_file=image_file)
  
  
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

@app.route('/upload_img', methods=['GET', 'POST'])
@login_required
def upload_img():
    if request.method == 'POST':
        file = request.files['file']
        exists = db.session.query(Upload).filter_by(user_id=current_user.id, doc_type="profile_pic").first()
        if exists:
            db.session.delete(exists)
        upload = Upload(filename=file.filename, data=file.read(), user_id=current_user.id, doc_type="profile_pic")
        db.session.add(upload)
        db.session.commit()

        return f'Uploaded: {file.filename}'
    return render_template('index.html')

@app.route('/upload_resume', methods=['GET', 'POST'])
@login_required
def upload_resume():
    if request.method == 'POST':
        file = request.files['file']
        
        upload = Upload(filename=file.filename, data=file.read(), user_id=current_user.id, doc_type="resume")
        db.session.add(upload)
        db.session.commit()

        return f'Uploaded: {file.filename}'
    return render_template('index.html')

#---------------------------------------------------------- Profiles --------------------------------------------------------------------------#


#-------------- Uploading Documents -------------------------#
@app.route('/download/<upload_id>')
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data), attachment_filename=upload.filename, as_attachment=True)
#-------------- Uploading Documents -------------------------#
        
#-------------------------------------------------------------Jobs---------------------------------------------------------------#
@app.route('/jobs')
@login_required
def jobs():
    if current_user.is_authenticated:
        title = db.session.query(Job).filter
    return render_template('jobs.html', job_title=title)
  
  
  
@app.route('/create_job', methods=['GET', 'POST'])
@login_required
def add_job():
    if is_recruiter() or is_admin():
        form = AddJob()
        if form.validate_on_submit():
            fk_recruiter_id =db.session.query(Recruiter).filter_by(id=1).first()
            job_title = form.job_title.data
            company = form.company.data
            description = form.job_description.data
            url = form.job_url.data
            job_posting = Job(job_title=job_title, company=company, job_description=description, job_url=url, fk_recruiter_id=fk_recruiter_id.id)
            db.session.add(job_posting)
            db.session.commit()
            #all_jobs= db.session.query(Job.job_title).all()
            #print(all_jobs, file=sys.stderr)
        flash('Job Posted!')
        return render_template('create_jobs.html', form=form)
        
    return render_template('invalid_credentials.html')

@app.route('/apply_job/<job_id>', methods=['GET', 'POST'])
@login_required
def apply_job(job_id):
    if is_student():
        # form=ApplyJob()
        fk_job_id = job_id

        exists = db.session.query(Upload.id).filter_by(user_id=current_user.id, doc_type="resume").first() is not None
        if exists:
            A_resume = db.session.query(Upload).filter_by(user_id=current_user.id, doc_type="resume", fk_job_id=fk_job_id).with_entities(Upload.data).first()

        #Application variable stores final information to be added to the database (association tables)
        application = Associations_Application(fk_user_id=current_user.id, fk_job_id=fk_job_id)
        db.session.add(application)
        db.session.commit()
        # print(job_id, file = sys.stdout)
        return render_template('application.html')
        
    return render_template('invalid_credentials.html')
#API / SEARCH (API is on top of the file)
#-----------------------API SECTION------------------------------------------------------------#
@app.route('/search', methods=['GET', 'POST'])
def search():
    headers =   {'Host': API_HOST,
                'User-Agent': EMAIL,
                'Authorization-Key': API_KEY}
    form = SearchForm()
    if form.validate_on_submit():
        job_results = []
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

        for item in db.session.query(Job).filter(Job.job_title==keyword):
            # job_retrieved = 'internal'
            job = JobInfo() #this class is located in models.py, it does not create a table and is not used (investigate)
            job.retrieved = 'internal'
            job.id = item.id
            job.title = item.job_title
            job.URI = item.job_url
            job.location = item.company
            job_results.append(job)

        response_json = response.json()
        
        
        for item in response_json['SearchResult']['SearchResultItems']:
            # job_retrieved = 'external'
            job = JobInfo()
            job.retrieved = 'external'
            job.URI = item['MatchedObjectDescriptor']['PositionURI']
            job.title = item['MatchedObjectDescriptor']['PositionTitle']
            job.location = item['MatchedObjectDescriptor']['PositionLocationDisplay']
            job_results.append(job)

         # display search results as an HTML table
        return render_template('view_jobs.html', job_results=job_results)
    else:
        return render_template('search.html', form=form)
#------------------------ API SECTION -------------------------------------------------------------#
#-------------------------------------------------------------Jobs---------------------------------------------------------------#
                           
                         


#---------------------App Error--------------------------------------------------------------------#
#page not found
@app.errorhandler(404)
def error404(error):
    return render_template('404.html'), 404

#failed db conenction
@app.errorhandler(500)
def error500(error):
    return render_template('500.html'), 500
#---------------------App Error--------------------------------------------------------------------#



#-----------STANDALONE FUNCTION SECTION--------------#
#Role Validation-------------------------------------#
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
#---------------------------------------------------#







