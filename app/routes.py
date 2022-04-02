from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import AccountRecovery, LoginForm, ChangePasswordForm, CreateUserForm
from app import db
from app.models import User
import sys

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

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

@app.route('/add_user', methods=['GET', 'POST'])
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
    return render_template('add_user.html', form=form)

@app.route('/jobs')
@login_required
def jobs():
    return render_template('jobs.html')

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

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

@app.route('/account_recovery', methods=['GET', 'POST'])
@login_required
def recover_account():
    form = AccountRecovery()
    if form.validate_on_submit():
        username = form.username.data
        if db.session.query(User).filter_by(username=username).first():
            print("Account Recovered")
    return render_template('account_recovery.html', form=form)

