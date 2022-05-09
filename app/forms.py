#imports
from wsgiref.validate import validator
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from wtforms.widgets import TextArea
from flask_wtf.file import FileField
from app import *


#----------------------New User Creation--------------------------------------------------#
class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    role = SelectField('Role', choices=[('student', 'student'), ('faculty', 'faculty'), ('recruiter', 'recruiter'), ('regular','regular')])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    mname = StringField('MI')
    company_name = StringField('Company (Not relevant if not recruiter)')
    profile_pic = FileField('Profile Picture')
    date_of_birth = DateField('Date of Birth (YYYY/MM/DD) (In Progress)')
    submit = SubmitField('Create Account')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValueError('TAKEN')
    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValueError('TAKEN')
#----------------------New User Creation--------------------------------------------------#


#------------------Logging into Shrimpedin--------------------#
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Require a login input")])
    password = PasswordField('Password', validators=[DataRequired(message="Require a password")])
    submit = SubmitField('Sign In')
    #add the create account button
    #add the account recovery button
#------------------Logging into Shrimpedin--------------------#



#----------------------Account settings----------------------------------------------------#
class ChangePasswordForm(FlaskForm):
    old_pass = PasswordField('Old password', validators=[DataRequired(message="please enter your old password")])
    new_pass = PasswordField('New password', validators=[DataRequired(message="please")])
    new_pass_retype = PasswordField('Retype new password', validators=[DataRequired()])
    submit = SubmitField('Change password')

    
class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    role = SelectField('Role', choices=[('student', 'student'), ('faculty', 'faculty'), ('recruiter', 'recruiter')])
    fname = StringField('First Name', validators=[DataRequired()])#length(min=2, max=64) Testing stuff with min and max length
    lname = StringField('Last Name', validators=[DataRequired()])
    mname = StringField('MI')
    company_name = StringField('Company (Not relevant if not recruiter)')
    profile_pic = FileField('Profile Picture')
    date_of_birth = DateField('Date of Birth')
    submit = SubmitField('Create Account')
    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValueError('TAKEN')

class EditProfileForm(FlaskForm):
    phone_number = StringField('Phone Number')
    address = StringField('Street Address')
    city = StringField('City')
    state = SelectField('State', choices=['', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 
                                        'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS',
                                         'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 
                                         'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 
                                         'WI', 'WY'])
    zip_code = StringField('Zip Code')
    phone_number = StringField('Phone Number')
    fname = StringField('First Name')
    mname = StringField('Middle Initial')
    user_bio = StringField('User Bio', widget=TextArea())
    lname = StringField('Last Name')
    profile_pic = FileField('Profile Picture')
    submit = SubmitField('Update Profile')

   

class AccountRecovery(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Recover Account')

class RemoveUser(FlaskForm):
    # job_id = IntegerField('Enter Job ID number', validators=[DataRequired()])
    submit = SubmitField('Submit')
#----------------------Account settings----------------------------------------------------#



#----------------job forms------------------#
class AddJob(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()])
    salary = DecimalField('Salary Ammount Per Year', places=2)
    job_description = StringField('Description', validators=[DataRequired()])
    job_url = StringField('Job URL')
    job_address = StringField('Job Location Address')
    job_city = StringField('Job Location City')
    job_state = SelectField('State', choices=['', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 
                                        'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS',
                                         'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 
                                         'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 
                                         'WI', 'WY'])
    job_zipcode = StringField('Job Location Zipcode')
    submit = SubmitField('Submit')
    

class ApplyJob(FlaskForm):
    
    submit = SubmitField('Submit')


class EditJob(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()])
    job_description = StringField('Job Description', validators=[DataRequired()])
    job_url = StringField('Job URL', validators=[DataRequired()])
    job_salary = DecimalField('Salary Amount Per Year', places=2)
    job_address = StringField('Job Location Address')
    job_city = StringField('Job Location City')
    job_state = SelectField('State', choices=['', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 
                                        'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS',
                                         'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 
                                         'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 
                                         'WI', 'WY'])
    job_zipcode = StringField('Job Location Zipcode')
    submit = SubmitField('Submit')

class RemoveJob(FlaskForm):
    # job_id = IntegerField('Enter Job ID number', validators=[DataRequired()])
    submit = SubmitField('Submit')
#----------------job forms------------------#




#--------------- Search Form -------------------------#
class SearchForm(FlaskForm):
     keyword = StringField('Keyword', validators=[DataRequired()])
     city = StringField('City', validators=[DataRequired()])
     state = StringField('State', validators=[DataRequired()])
     submit = SubmitField('Search')

class SearchForm2(FlaskForm):
    keyword = StringField('Keyword', validators=[DataRequired()])
    submit = SubmitField('Search')
#--------------- Search Form -------------------------#


# #------------------upload form--------------------#
# class Upload_IMG_Form(FlaskForm):
#     img_file = FileField('Upload Image', validators=[FileAllowed(['jpg','png'])])
#     submit = SubmitField('Submit')
# #------------------upload form--------------------#