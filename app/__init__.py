from flask import Flask
from flask_login import LoginManager
import os

app = Flask(__name__)
app.debug=True
app.config['DATABASE'] = os.path.join(app.root_path, "db/database.db")
app.config['SECRET_KEY'] = "verysecret"
login_manager = LoginManager(app)
login_manager.login_view = "login"


from app import dbase, authentication, routes