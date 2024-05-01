from app import db
from datetime import datetime
from flask_login import UserMixin


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
