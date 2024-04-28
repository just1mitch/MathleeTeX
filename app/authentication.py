from app import app, login_manager
from flask import Flask, flash
from flask_login import UserMixin
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError

from app.dbase import get_db, close_db

class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

        

class SignUpForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired(), Email()])
    username = StringField('Username:', validators=[DataRequired(), Length(min=3, max=30, message="Username must be between 3-30 characters"), Regexp("^\w+$", \
                                                                                                  message="Username must contain only Letters, numbers or underscores")])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, message="Password must contain more than 8 characters"), Regexp("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", \
                                                                                            message="Password must contain at least:\none letter, one number, and one special character.")])
    confirm = PasswordField('Repeat Password:', validators=[DataRequired(), EqualTo(password, message="Passwords do not match.")])


    
class User(UserMixin):
    def __init__(self, user_id, username, email, password):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.authenticated = False

    def is_authenticated(self):
        return self.authenticated
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.user_id


@login_manager.user_loader
def load_user(user_id):
    curs = get_db()
    curs.execute("SELECT * FROM users WHERE user_id = (?)", [user_id])
    lu = curs.fetchone()
    if lu is None:
        return None
    else:
        return User(lu[0], lu[1], lu[2], lu[3])
    

def validate_login(username, password):
    curs = get_db()
    curs.execute("SELECT * FROM users WHERE username = (?)", [username])
    usr_data = curs.fetchone()
    if usr_data is None:
        flash('Username does not exist')
        return None
    else:
        usr_data = list(usr_data)
        Usr = load_user(usr_data[0])
        if username == Usr.username and password == Usr.password:
            return Usr
        else:
            flash('Incorrect Password')
            return None

