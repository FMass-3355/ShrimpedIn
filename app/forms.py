#===================================================================================================
#Imports
#===================================================================================================
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
#===================================================================================================








class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
    #add the create account button
    #add the account recovery button

class ChangePasswordForm(FlaskForm):
    old_pass = PasswordField('Old password', validators=[DataRequired()])
    new_pass = PasswordField('New password', validators=[DataRequired()])
    new_pass_retype = PasswordField('Retype new password', validators=[DataRequired()])
    submit = SubmitField('Change password')

class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    role = SelectField('Role', choices=[('student', 'student'), ('faculty', 'faculty'), ('recruiter', 'recruiter')])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    mname = StringField('MI')
    date_of_birth = DateField('Date of Birth (YYYY/MM/DD) (In Progress)')
    submit = SubmitField('Create Account')


class EditProfileForm(FlaskForm):
    address = StringField('Street Address')
    city = StringField('City')
    state = StringField('State')
    zip_code = StringField('Zip Code')
    submit = SubmitField('Complete Edits')


class AccountRecovery(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Recover Account')







class AddJob(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    job_description = StringField('Description', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
     keyword = StringField('Keyword', validators=[DataRequired()])
     city = StringField('City', validators=[DataRequired()])
     state = StringField('State', validators=[DataRequired()])
     submit = SubmitField('Search')

class SearchForm2(FlaskForm):
    keyword = StringField('Keyword', validators=[DataRequired()])
    submit = SubmitField('Search')

