from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired

class AddForm(FlaskForm):
    city = StringField('City:', validators=[DataRequired()])
    population = IntegerField('Population: ', validators=[DataRequired()])
    submit = SubmitField('Save')

class DeleteForm(FlaskForm):
    city = StringField('City:', validators=[DataRequired()])
    submit = SubmitField('Delete')

class SearchForm(FlaskForm):
    city = StringField('City:', validators=[DataRequired()])
    submit = SubmitField('Search')

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
    submit = SubmitField('Create Account')

class AccountRecovery(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Recover Account')
