from flask_login import current_user
from app.models import comments
from app import db

def add_comment(qid, comment_form):
    new_comment = comments(question_id=qid,
                           user_id=current_user.get_id(),
                           body=comment_form.comment.data)
    db.session.add(new_comment)
    db.session.commit()
    return