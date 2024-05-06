from app import app
from flask import render_template, url_for, request, redirect

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login_signup.html")
    else:
        #POST request - client-end validation succeeded
        return redirect(url_for("index"))
    
@app.route("/signup", methods=['POST'])
def signup_user():
    #POST request - client-end validation
    return redirect(url_for("index"))

@app.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html")

@app.route("/create")
def make_quiz():
    return render_template("makeQuiz.html")

@app.route("/play")
def play_quiz():
    return render_template("playQuiz.html")