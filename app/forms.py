#===================================================================================================
#Imports
#===================================================================================================
from secrets import choice
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
#===================================================================================================

#===================================================================================================
#Accounts Section
#===================================================================================================
#===================================================================================================
#Logging in Form
#===================================================================================================
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
    #add the create account button
    #add the account recovery button
#===================================================================================================

#===================================================================================================
#Change Password Form
#===================================================================================================
class ChangePasswordForm(FlaskForm):
    old_pass = PasswordField('Old password', validators=[DataRequired()])
    new_pass = PasswordField('New password', validators=[DataRequired()])
    new_pass_retype = PasswordField('Retype new password', validators=[DataRequired()])
    submit = SubmitField('Change password')
#===================================================================================================

#===================================================================================================
#Create User Form
#===================================================================================================
class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    role = SelectField('Role', choices=[('student', 'student'), ('faculty', 'faculty'), ('recruiter', 'recruiter')])
    fname = StringField('First Name', validators=[DataRequired()])#length(min=2, max=64) Testing stuff with min and max length
    lname = StringField('Last Name', validators=[DataRequired()])
    mname = StringField('MI')
    date_of_birth = DateField('Date of Birth')
    submit = SubmitField('Create Account')
    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValueError('TAKEN')
#===================================================================================================

#===================================================================================================
# EDIT PROFILE A WORK IN PROGRESS
#===================================================================================================
class EditProfileForm(FlaskForm):
    phone_number = StringField('Phone Number')
    address = StringField('Street Address')
    city = StringField('City')
    state = SelectField('State', choices=['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 
                                        'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS',
                                         'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 
                                         'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 
                                         'WI', 'WY'])
    zip_code = StringField('Zip Code')
    phone_number = StringField('Phone Number')
    fname = StringField('First Name')
    m_name = StringField('Middle Initial')
    lname = StringField('Last Name')
    email = StringField('Email')
    username = StringField('Username')
    submit = SubmitField('Update Profile')
#===================================================================================================

#===================================================================================================
#Account Recovery Form
#===================================================================================================
class AccountRecovery(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Recover Account')
#===================================================================================================
#===================================================================================================





#For Jobs such as adding and Searching
#===================================================================================================
#Add Job Form
#===================================================================================================
class AddJob(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    job_description = StringField('Description', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    submit = SubmitField('Submit')
#===================================================================================================

#===================================================================================================
#search jobs form
#===================================================================================================
class SearchForm(FlaskForm):
     keyword = StringField('Keyword', validators=[DataRequired()])
     city = StringField('City', validators=[DataRequired()])
     state = StringField('State', validators=[DataRequired()])
     submit = SubmitField('Search')
#===================================================================================================    

class SearchForm2(FlaskForm):
    keyword = StringField('Keyword', validators=[DataRequired()])
    submit = SubmitField('Search')

