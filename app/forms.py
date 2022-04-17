#===================================================================================================
#Imports
#===================================================================================================
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, StringField, PasswordField, FloatField
from wtforms.validators import DataRequired
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
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Create Account')
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

