from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user, logout_user
from flask_login import login_user
from sqlalchemy import inspect, func


from app import app, db
from app.models import users, questions, user_answers, comments, LoginForm, SignupForm, QuestionForm, AnswerForm


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

@app.route('/play', methods=['GET'])
def play():
    page = request.args.get('page', 1, type=int)
    # Query database for all questions
    # Join user information to the questions
    # If user is signed in, don't display questions posted by them
    # They can view these on the profile page, and shouldnt be able to answer
    # their own questions anyways
    user = current_user.get_id()
    if user is not None:
        query = db.session.query(questions, users).join(users).filter(questions.user_id != user)
    else:
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
    answer_form = AnswerForm()
    
    return render_template("play_question.html", question_list=question_list, answer_form=answer_form)

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
    return(render_template('create_question.html', question_form=question_form))

@app.route('/leaderboard')
def leaderboard():
    return(render_template('leaderboard.html'))

@app.route('/answer_question/<qid>', methods=["GET"])
@login_required
def answer_question(qid):
    # Get question information
    question = questions.query.filter_by(question_id=qid).first()
    code = question.correct_answer
    # Get users attempt amounts
    attempts = user_answers.query.filter(user_answers.user_id == current_user.get_id(), user_answers.question_id == qid).count()
    # Get boolean if user has answered correctly
    if(user_answers.query.filter(user_answers.user_id == current_user.get_id(), user_answers.question_id == qid, user_answers.is_correct == True).first()) is not None:
        completed = True
    else: completed = False
    response = {
        'code': code,
        'attempts': attempts,
        'completed': completed
    }
    return response

@app.route('/check_answer/<qid>', methods=["POST"])
def check_answer(qid):
    answer_form = AnswerForm(request.form)
    if answer_form.validate_on_submit():
        answer = answer_form.answer.data
        attempts = user_answers.query.filter(user_answers.user_id == current_user.get_id(), user_answers.question_id == qid).count()
        # Add attempt to database
        new_attempt = user_answers(question_id=qid,
                                   user_id=current_user.get_id(),
                                   answer_text = answer,
                                   attempt_number = attempts + 1)
        correct_answer = questions.query.filter_by(question_id=qid).first().correct_answer
        
        new_attempt.is_correct = correct_answer == answer

        # Calculate points earned
        difficulty = questions.query.filter(questions.question_id == qid).first().difficulty_level
        if difficulty == 'Easy':
            points = max(0, 3 - attempts)
        elif difficulty == 'Medium':
            points = max(0, 6 - attempts * 2)
        else:
            points = max(0, 9 - attempts * 3)
        
        response = {
            'completed': new_attempt.is_correct,
            'points': points
        }
        
        # Commit to database and return results
        if(new_attempt.is_correct):
            # Add points to users total if the answer was correct
            user = users.query.filter(users.user_id == current_user.get_id()).first()
            user.points += points
        db.session.add(new_attempt)
        db.session.commit()
        return response
    return
