from app import app, login_manager
from flask import Flask, render_template, url_for, request, redirect, Response
from flask_login import UserMixin, login_required, login_user, logout_user, current_user
from app.authentication import LoginForm, SignUpForm, validate_login
from app.dbase import get_db, close_db


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        Usr = validate_login(form.username.data, form.password.data)
        if Usr is not None:
            login_user(Usr, remember=form.remember.data)
            return redirect(request.args.get('next') or url_for('home'))
    return render_template('login.html', form=form)

@app.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html")

@app.route("/create")
@login_required
def makeQuiz():
    return render_template("makeQuiz.html")

@app.route("/play")
@login_required
def playQuiz():
    return render_template("playQuiz.html")