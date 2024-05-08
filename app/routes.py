from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user, logout_user
from flask_login import login_user
from app import app, db
from app.models import users, questions, user_answers, comments, LoginForm, SignupForm
from sqlalchemy import inspect

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

#Login attempts are directed here
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    login_form = LoginForm()
    signup_form = SignupForm()
    #Process submitted form
    if login_form.validate_on_submit():
        usr = users.query.filter_by(username=login_form.username.data).first()
        if usr is not None and usr.password == login_form.password.data:
            login_user(usr, remember=login_form.remember.data)
            return redirect(request.args.get('next') or url_for('profile'))
        else:
            flash('flash_login: Incorrect username or password. Please try again.', 'error')
    #Return login page for failed login and GET requests
    return render_template('login_signup.html', login_form=login_form, signup_form=signup_form)


#Signup attempts are directed here
@app.route('/signup', methods=['POST'])
def signup_user():
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        user_exists = users.query.filter_by(username=signup_form.setusername.data).first() is not None
        email_exists = users.query.filter_by(email=signup_form.setemail.data).first() is not None
        #Check for duplicate credentials
        if user_exists:
            #Username is taken
            print('username already exists')
            flash ('flash_signup: Username is taken. Please try again.')
        elif email_exists:
            #Email is taken
            flash ('flash_signup: Email is already in use. Please try again.')
        else:
            # Some kind of password store/hash thing should go here for now will just use the password as is
            new_user = users(username=signup_form.setusername.data, email=signup_form.setemail.data, password=signup_form.createpassword.data)
            db.session.add(new_user)
            db.session.commit()
            # Successful signup - automatically log the user in
            usr = users.query.filter_by(username=signup_form.setusername.data).first()
            login_user(usr)
            return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('login'))

@app.route('/play')
def play_quiz():
    return render_template("playQuiz.html")

@app.route('/create')
@login_required
def make_quiz():
    return render_template("makeQuiz.html")



@app.route('/list_tables')
def list_tables():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    return jsonify(tables)

@app.route('/list_columns/<table_name>')
def list_columns(table_name):
    inspector = inspect(db.engine)
    columns = inspector.get_columns(table_name)
    column_info = [{ 'name': col['name'], 'type': str(col['type']) } for col in columns]
    return jsonify(column_info)

@app.route('/list_users')
def list_users():
    user_array = []
    users_list = users.query.all()
    for user in users_list:
        user_array.append({
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'sign_up_date': user.sign_up_date,
            'points': user.points
        })
    return jsonify(user_array)

@app.route('/create', methods=["GET"])
def create():
    return(render_template('create_question.html'))

@app.route('/create', methods=["POST"])
def create_question():
    print("received POST")
    return

@app.route('/leaderboard')
def leaderboard():
    return(render_template('leaderboard.html'))

# @app.route('/list_questions')
# def list_questions():
#     questions_array = []
#     questions_list = questions.query.all()
#     for question in questions_list:
#         questions_array.append({
#             'question_id': question.question_id,
#             'user_id': question.user_id,
#             'title': question.title,
#             'question_description': question.question_description,
#             'correct_answer': question.correct_answer,
#             'date_posted': question.date_posted,
#             'difficulty_level': question.difficulty_level
#         })
#     return jsonify(questions_array)
