from app import db
from datetime import datetime
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError

# This class is for formatting/validating Login Form input - username, password, remember me
class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember Me:')
    submit = SubmitField('Login')

# This class is for formatting/validating Signup Form input - email, username, password, confirm password
class SignupForm(FlaskForm):
    setemail = EmailField('Email:', validators=[DataRequired()])
    setusername = StringField('Username:', validators=[DataRequired(), Length(min=3, max=20)])
    createpassword = PasswordField('Password:', validators=[DataRequired(), Length(min=8)])
    confirmpassword = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('createpassword')])

# This class is for formatting/validating Creating Question input - difficulty, title, description, code
class QuestionForm(FlaskForm):
    difficulty = RadioField('Select a Difficulty:', choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], default='Easy', validators=[DataRequired()])
    title = StringField('Question Title:', validators=[DataRequired(), Length(min=1)])
    description = TextAreaField('Question Description:', validators=[DataRequired(), Length(min=1)])
    code = StringField('Enter Your LaTeX Code:', validators=[DataRequired(), Length(min=1)])

# This class is for answering a question
class AnswerForm(FlaskForm):
    answer = StringField('Answer:', validators=[DataRequired(), Length(min=1)])

# This table is for storing user information - username, email, password, sign up date, and points
class users(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    sign_up_date = db.Column(db.DateTime, default=datetime.utcnow)
    points = db.Column(db.Integer, default=0)

    def get_id(self):
        return str(self.user_id)

# This table is for storing questions - user_id, title, question description, correct answer, date posted, and difficulty level
class questions(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    question_description = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    difficulty_level = db.Column(db.String, nullable=False)
    comments = db.relationship('comments', backref='questions')

# This table is for storing user answers - question_id, user_id, answer text, whether the answer is correct, attempt number, and date posted
class user_answers(db.Model):
    answer_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    attempt_number = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)


# This table is for storing comments - question_id, answer_id, user_id, comment body, and date posted
class comments(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('user_answers.answer_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
