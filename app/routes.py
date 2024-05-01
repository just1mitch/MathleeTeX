from flask import render_template, request, redirect, url_for, jsonify
from app import app, db
from app.models import users, questions, user_answers, comments
from sqlalchemy import inspect

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signupUser():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        return 'Passwords do not match', 400

    user_exists = users.query.filter_by(username=username).first() is not None
    email_exists = users.query.filter_by(email=email).first() is not None

    if user_exists:
        return 'Username already exists', 400
    if email_exists:
        return 'Email already exists', 400

    # Some kind of password store/hash thing should go here for now will just use the password as is
    new_user = users(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))


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