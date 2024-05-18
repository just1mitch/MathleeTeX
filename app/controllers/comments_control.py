from flask_login import current_user
from app.models import comments
from app import db

def add_comment(qid, comment_form):
    return