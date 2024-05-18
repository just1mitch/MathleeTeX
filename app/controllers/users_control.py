from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import users
from app import db

# Adds user to database from data in signup_form
# Returns a tuple (userdata, error) - where error is populated
# with an error message if unable to add user to database
def create_user(signup_form):
    user_exists = users.query.filter_by(username=signup_form.setusername.data).first() is not None
    email_exists = users.query.filter_by(email=signup_form.setemail.data).first() is not None
    #Check for duplicate credentials
    if user_exists:
        #Username is taken
        return(None, 'flash_signup: Username is taken. Please try again.')
    elif email_exists:
        #Email is taken
        return(None, 'flash_signup: Email is already in use. Please try again.')
    else:
        # Hash password before adding new user details to the database
        raw_pwd = signup_form.createpassword.data
        hashed_pwd = generate_password_hash(raw_pwd)
        new_user = users(username=signup_form.setusername.data, email=signup_form.setemail.data, password=hashed_pwd)
        db.session.add(new_user)
        db.session.commit()
        # Successful signup - pass user data back to calling function
        usr = users.query.filter_by(username=signup_form.setusername.data).first()
        return (usr, None)
    
# Attempts to log user in using data in login_form
# If an error occurs, return (False, errormessage)
# Else return (True, None)
def attempt_login(login_form):
    usr = users.query.filter_by(username=login_form.username.data).first()
    if usr is not None:
        pwd_hash = usr.password
        if check_password_hash(pwd_hash, login_form.password.data):
            login_user(usr, remember=login_form.remember.data)
            return (True, None)
        else:
            return(False, 'flash_login: Incorrect password.')
    else:
        return(False, 'flash_login: User not found.')