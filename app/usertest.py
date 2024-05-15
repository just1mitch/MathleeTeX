import random
from app import db
from app.models import users
from sqlalchemy.exc import IntegrityError

def create_users(n):
    for i in range(n):
        username = f"user_{i+1}"
        email = f"user_{i+1}@example.com"
        password = "password"
        points = random.randint(1, 100)

        new_user = users(username=username, email=email, password=password, points=points)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
