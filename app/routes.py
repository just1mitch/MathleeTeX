from flask import render_template, request, redirect, url_for, jsonify
from app import app, db
from app.models import users, questions, user_answers, comments
from sqlalchemy import inspect

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list_tables')
def list_tables():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    return jsonify(tables)

@app.route('/list_columns/<table_name>')
def list_columns(table_name):
    inspector = inspect(db.engine)
    columns = inspector.get_columns(table_name)
    return jsonify(columns)

@app.route('/list_users')
def list_users():
    users_list = users.query.all()
    return jsonify(users_list)