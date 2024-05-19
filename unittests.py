# test_app.py
import unittest
from app import app, db
from app.models import users, questions, user_answers, comments
from config import TestConfig
from werkzeug.security import generate_password_hash

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        # Setup app with test configuration
        app.config.from_object(TestConfig)
        self.client = app.test_client(use_cookies=True)
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_signup(self):
        response = self.client.post('/signup', data={
            'setemail': 'newuser@example.com',
            'setusername': 'newuser',
            'createpassword': 'ValidPass123#',
            'confirmpassword': 'ValidPass123#'
        }, follow_redirects=True)
        self.assertIn(b'Your Questions', response.data) # Only on the profile page
        self.assertEqual(users.query.count(), 1)

    def test_user_login(self):
        # First, create a user directly in the database
        password = generate_password_hash('ValidPass123#')
        user = users(username='testuser', email='test@example.com', password=password)
        db.session.add(user)
        db.session.commit()
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'ValidPass123#'
        }, follow_redirects=True)
        self.assertIn(b'Your Questions', response.data)

    def test_access_profile_unauthenticated(self):
        response = self.client.get('/profile', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_profile_page_authenticated(self):
        self.test_user_login()
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testuser', response.data)

    def test_create_question(self):
        self.test_user_login()
        response = self.client.post('/create', data={
            'difficulty': 'Easy',
            'title': 'Monkey Maths',
            'description': 'What is unit testing?',
            'code': 'bananas'
        }, follow_redirects=True)
        self.assertIn(b'Monkey Maths', response.data)
        self.assertEqual(questions.query.count(), 1)

    def test_delete_question(self):
        self.test_create_question()
        question_id = questions.query.first().question_id
        response = self.client.post(f'/delete_question/{question_id}', follow_redirects=True)
        self.assertIn('true', str(response.data))

if __name__ == '__main__':
    unittest.main()
