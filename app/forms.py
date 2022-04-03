from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, StringField, PasswordField, FloatField
from wtforms.validators import DataRequired
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
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Create Account')

class AccountRecovery(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Recover Account')

class AddJob(FlaskForm):
    Company=StringField('Company Name', validators=[DataRequired()])
    Job_title=StringField('Enter', validators=[DataRequired()])
    Job_site=StringField('Location of Job', validators=[DataRequired()])
    Salary=FloatField('Salary',validators=[DataRequired()])


