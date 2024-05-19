from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user, logout_user
from flask_login import login_user
from flask_paginate import Pagination, get_page_args
from sqlalchemy import inspect, func
from .testing.usertest import create_users

from app import app, db
from app.models import users, questions, user_answers, comments, LoginForm, SignupForm, QuestionForm, AnswerForm, CommentForm
from app.controllers import users_control, questions_control, user_answers_control, comments_control

@app.route('/')
def index():
    top_users = users.query.order_by(users.points.desc()).limit(5).all() # Get top 5 users
    return render_template('index.html', top_users=top_users)


@app.route('/profile')
@login_required
def profile():
    user_questions = questions.query.filter_by(user_id=current_user.user_id).all()
    # filter out deleted questions
    user_questions = [q for q in user_questions if not q.deleted]
    # Get the number of attempts and comments for each question
    for question in user_questions:
        # changed this to just use the count method based on the user_answers table - simpler than a large join
        question.num_attempts = user_answers.query.filter_by(question_id=question.question_id).count()
        question.num_comments = comments.query.filter_by(question_id=question.question_id).count()
    rank = None
    if current_user.is_authenticated:
        if rank is None:
            rank = users.query.filter(users.points > current_user.points).count() + 1
            current_user_stats = {
            'username': current_user.username,
            'points': current_user.points,
            'date_joined': current_user.sign_up_date.strftime('%Y-%m-%d'),
            'questions_answered_correctly': current_user.questions_answered_correctly,
            'total_questions_answered': current_user.total_questions_answered,
            'rank': rank
        }
        answer_form = AnswerForm()
        recent_comments = comments.query.filter(current_user.get_id() == comments.user_id).order_by(comments.date_posted.desc()).limit(5)
        recent_comments = recent_comments.with_entities(comments.body,
                                                        comments.date_posted)
    return render_template('profile.html', user_questions=user_questions, current_user_stats=current_user_stats, answer_form=answer_form, recent_comments=recent_comments)

#Login attempts are directed here
@app.route('/login', methods=['GET', 'POST'])
def login():
    create_users(20)
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    login_form = LoginForm()
    signup_form = SignupForm()
    #Process submitted form
    if login_form.validate_on_submit():
        (success, error) = users_control.attempt_login(login_form)
        if success:
            return redirect(request.args.get('next') or url_for('profile'))
        else:
            flash(error)
    #Return login page for failed login and GET requests
    return render_template('login_signup.html', login_form=login_form, signup_form=signup_form)


#Signup attempts are directed here
@app.route('/signup', methods=['POST'])
def signup_user():
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        (usr, error) = users_control.create_user(signup_form)
        if error is not None:
            flash(error)
        else:
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
    
    # Filter out deleted questions
    query = query.filter(questions.deleted == False)
    
    query = query.outerjoin(comment_count, comment_count.c.question_id==questions.question_id)

    question_list = query.with_entities(questions.question_id,
                                        questions.title,
                                        questions.question_description,
                                        questions.difficulty_level,
                                        questions.date_posted,
                                        users.username,
                                        comment_count.c.comment_count
                                        ).order_by(questions.date_posted.desc()).paginate(page=page, per_page=10)
    answer_form = AnswerForm()
    
    return render_template("play_question.html", question_list=question_list, answer_form=answer_form)

@app.route('/create', methods=["GET", "POST"])
@login_required
def create():
    question_form = QuestionForm()
    if question_form.validate_on_submit():
        questions_control.add_question(question_form)
        return redirect(url_for('profile'))
    return(render_template('create_question.html', question_form=question_form))

def get_users(offset=0, per_page=10):
    return users.query.order_by(users.points.desc()).slice(offset, offset + per_page).all()


@app.route('/delete_question/<int:qid>', methods=['POST'])
@login_required
def delete_question(qid):
    # Get the question to delete - we'll use AJAX to send the request
    question = questions.query.get_or_404(qid)
    if current_user.user_id != question.user_id:
        return jsonify({'error': 'You are not auth to delete this question.'}), 403

    # set the deleted boolean to True
    question.deleted = True
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/leaderboard')
def leaderboard():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = users.query.count()

    show_me = 'show_me' in request.args
    if current_user.is_authenticated and show_me:
        rank = users.query.filter(users.points > current_user.points).count() + 1
        calculated_page = (rank - 1) // per_page + 1

        # Redirect if show_me is set but a specific page is also requested
        if request.args.get('page') and int(request.args.get('page')) != calculated_page:
            return redirect(url_for('leaderboard', page=request.args.get('page')))
        page = calculated_page
        offset = (page - 1) * per_page


    user_list = get_users(offset=offset, per_page=per_page)

    # init rank with a default value
    rank = None
    if current_user.is_authenticated and request.args.get('show_me'):
        rank = users.query.filter(users.points > current_user.points).count() + 1
        page = (rank - 1) // per_page + 1
        offset = (page - 1) * per_page
        user_list = get_users(offset=offset, per_page=per_page)

    pagination = Pagination(page=page, per_page=per_page, total=total)

    current_user_stats = None


    if current_user.is_authenticated:
        if rank is None:
            rank = users.query.filter(users.points > current_user.points).count() + 1
        current_user_stats = {
            'username': current_user.username,
            'points': current_user.points,
            'date_joined': current_user.sign_up_date.strftime('%Y-%m-%d'),
            'questions_answered_correctly': current_user.questions_answered_correctly,
            'total_questions_answered': current_user.total_questions_answered,
            'rank': rank
        }

    return render_template('leaderboard.html', users=user_list, page=page,
                           per_page=per_page, pagination=pagination, current_user_stats=current_user_stats)

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
        'completed': completed,
        'points': user_answers_control.points_available(qid, attempts)
    }
    return response

@app.route('/check_answer/<qid>', methods=["POST"])
def check_answer(qid):
    if current_user.is_authenticated:
        answer_form = AnswerForm(request.form)
        if answer_form.validate_on_submit():
            response = user_answers_control.add_attempt(qid, answer_form)
            return response
    return jsonify({'message': 'Unauthorized: Must be signed in'}), 401

@app.route('/get_comments/<qid>', methods=["GET"])
def get_comments(qid):
    comment_form = CommentForm()
    question_comments = comments.query.filter(comments.question_id==qid).join(users)
    question_comments = question_comments.with_entities(users.username,
                                                        comments.body,
                                                        comments.date_posted).order_by(comments.date_posted.desc()).limit(25)
    return render_template('comments_section.html', comment_form=comment_form, question_comments=question_comments)

@app.route('/create_comment/<qid>', methods=["POST"])
def create_comment(qid):
    if current_user.is_authenticated:
        comment_form = CommentForm(request.form)
        comments_control.add_comment(qid, comment_form)
        return jsonify({'message': 'Comment created successfully'}), 201
    return jsonify({'message': 'Unauthorized: Must be signed in'}), 401