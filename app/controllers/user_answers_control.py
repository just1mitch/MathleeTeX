from flask_login import current_user
from app.models import questions, user_answers, users
from app import db


def add_attempt(qid, answer_form):
    answer = answer_form.answer.data
    attempts = user_answers.query.filter(user_answers.user_id == current_user.get_id(), user_answers.question_id == qid).count()
    
    # Add attempt to database
    new_attempt = user_answers(question_id=qid,
                            user_id=current_user.get_id(),
                            answer_text = answer,
                            attempt_number = attempts + 1)
    correct_answer = questions.query.filter_by(question_id=qid).first().correct_answer
    
    new_attempt.is_correct = correct_answer == answer

    # If attempt is correct, points = points earned
    # If incorrect, points = new amount of points available
    # Commit to database and return results
    if(new_attempt.is_correct):
        # Add points to users total if the answer was correct
        user = users.query.filter(users.user_id == current_user.get_id()).first()
        points = points_available(qid, attempts)
        user.points += points
    else: points = points_available(qid, attempts + 1)
    
    db.session.add(new_attempt)
    db.session.commit()
    
    response = {
        'completed': new_attempt.is_correct,
        'points': points,
        'attempts': attempts + 1
    }
    return response

# Given a question id and the number of attempts, calculate the number of points
# that a user is able to earn on the question
def points_available(question_id, attempts):
    difficulty = questions.query.filter(questions.question_id == question_id).first().difficulty_level
    if difficulty == 'Easy':
        points = max(1, 3 - attempts)
    elif difficulty == 'Medium':
        points = max(1, 6 - attempts * 2)
    else:
        points = max(1, 9 - attempts * 3)
    return points