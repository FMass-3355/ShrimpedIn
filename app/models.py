from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# User extends the flask_login defined UserMixin class.  UserMixin
# provides default functionality that allows us to keep track of
# authenticated user
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    role = db.Column(db.String(64))
    password_hash = db.Column(db.String(256), unique=True)

    # ADDING
    fname = db.Column(db.String(64))
    lname = db.Column(db.String(64))

    def set_password(self, password):
        # Store hashed (encrypted) password in database
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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

    #address = db.Column(db.String(64))
    #zip_code = db.Column(db.Integer(5)) #imad didnt have () so might not work
    #city = db.Column(db.String(64))
    #state = db.Column(db.String(64)) #want to have a drop down list that can fill in state

    #resume *maybe*
    #cover_letter *maybe*
    #recomendation(s) ***maybe*** <--might need another table



# load_user is a function that's used by flask_login to manage the session.
# It simply returns the object associated with the authenticated user.
@login.user_loader
def load_user(id):
    return db.session.query(User).get(int(id))


class JobInfo:
    def __JobInfo__(title, URI, location):
        title = title
        URI = URI
        location = location