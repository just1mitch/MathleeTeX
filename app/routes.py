from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user, logout_user
from flask_login import login_user
from sqlalchemy import inspect, func
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from app.models import users, questions, user_answers, comments, LoginForm, SignupForm, QuestionForm


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
        if usr is not None:
            pwd_hash = usr.password
            if check_password_hash(pwd_hash, login_form.password.data):
                login_user(usr, remember=login_form.remember.data)
                return redirect(request.args.get('next') or url_for('profile'))
            else:
                flash('flash_login: Incorrect password.')
        else:
            flash('flash_login: User not found.')
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
            # Hash password before adding new user details to the database
            raw_pwd = signup_form.createpassword.data
            hashed_pwd = generate_password_hash(raw_pwd)
            new_user = users(username=signup_form.setusername.data, email=signup_form.setemail.data, password=hashed_pwd)
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

@app.route('/play', methods=['GET'])
def play():
    page = request.args.get('page', 1, type=int)
    # Query database for all questions
    # Join user information to the questions
    query = db.session.query(questions, users).join(users)
    comment_count = db.session.query(questions.question_id, func.count(questions.question_id).label("comment_count")).join(questions.comments).group_by(questions.question_id).subquery('comment_count')
    query = query.outerjoin(comment_count, comment_count.c.question_id==questions.question_id)

    question_list = query.with_entities(questions.question_id,
                                        questions.title,
                                        questions.question_description,
                                        questions.difficulty_level,
                                        questions.date_posted,
                                        users.username,
                                        comment_count.c.comment_count
                                        ).paginate(page=page, per_page=10)
    
    return render_template("play_question.html", question_list=question_list)

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
            #'password': user.password,
            'sign_up_date': user.sign_up_date,
            'points': user.points
        })
    return jsonify(user_array)

@app.route('/list_questions')
def list_questions():
    question_array = []
    question_list = questions.query.all()
    for question in question_list:
        question_array.append({
            'question_id': question.question_id,
            'user_id': question.user_id,
            'title': question.title,
            'question_description': question.question_description,
            'correct_answer': question.correct_answer,
            'date_posted': question.date_posted,
            'difficulty': question.difficulty_level
        })
    return jsonify(question_array)

@app.route('/create', methods=["GET", "POST"])
@login_required
def create():
    question_form = QuestionForm()
    if question_form.validate_on_submit():
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
        return redirect(url_for('play'))
    else:
        print(question_form.errors)
    return(render_template('create_question.html', question_form=question_form))

@app.route('/leaderboard')
def leaderboard():
    return(render_template('leaderboard.html'))

