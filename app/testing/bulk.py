from app import db
from app.models import users, questions, user_answers, comments
import random
from datetime import datetime, timedelta

def add_users(n):
    for _ in range(n):
        username = f"user{random.randint(1000, 9999)}"
        email = f"{username}@example.com"
        password = "Password"
        sign_up_date = datetime.utcnow() - timedelta(days=random.randint(0, 365))
        points = random.randint(0, 200)

        user = users(username=username, email=email, password=password, sign_up_date=sign_up_date, points=points)
        db.session.add(user)
    db.session.commit()

def add_questions(n):
    user_ids = [user.user_id for user in users.query.all()]
    for _ in range(n):
        user_id = random.choice(user_ids)
        title = f"Question {random.randint(100, 999)}"
        question_description = "This is a question with LaTeX formatting!"
        correct_answer = "2+2"
        date_posted = datetime.utcnow() - timedelta(days=random.randint(0, 365))
        difficulty_level = random.choice(['Easy', 'Medium', 'Hard'])

        question = questions(user_id=user_id, title=title, question_description=question_description, correct_answer=correct_answer, date_posted=date_posted, difficulty_level=difficulty_level)
        db.session.add(question)
    db.session.commit()

def add_user_answers(n):
    question_ids = [question.question_id for question in questions.query.all()]
    user_ids = [user.user_id for user in users.query.all()]
    for _ in range(n):
        question_id = random.choice(question_ids)
        user_id = random.choice(user_ids)
        answer_text = "Answer to the question"
        is_correct = random.choice([True, False])
        attempt_number = 1
        date_posted = datetime.utcnow() - timedelta(days=random.randint(0, 365))

        answer = user_answers(question_id=question_id, user_id=user_id, answer_text=answer_text, is_correct=is_correct, attempt_number=attempt_number, date_posted=date_posted)
        db.session.add(answer)
    db.session.commit()

def add_comments(n):
    question_ids = [question.question_id for question in questions.query.all()]
    user_ids = [user.user_id for user in users.query.all()]
    for _ in range(n):
        question_id = random.choice(question_ids)
        user_id = random.choice(user_ids)
        body = "This is a random comment!"
        date_posted = datetime.utcnow() - timedelta(days=random.randint(0, 365))

        comment = comments(question_id=question_id, user_id=user_id, body=body, date_posted=date_posted)
        db.session.add(comment)
    db.session.commit()

add_users(100)
add_questions(200)
add_user_answers(500)
add_comments(300)
