from app.models import questions
from app import db
from flask_login import current_user

# Adds a question to the questions database
# Using the data passed in through the question_form
def add_question(question_form):
    difficulty = question_form.difficulty.data
    title = question_form.title.data
    description = question_form.description.data
    code = question_form.code.data
    # Enter question into database
    new_question = questions(user_id=int(current_user.get_id()),
                                title=title,
                                question_description=description,
                                correct_answer=code,
                                difficulty_level=difficulty)
    db.session.add(new_question)
    db.session.commit()
    return