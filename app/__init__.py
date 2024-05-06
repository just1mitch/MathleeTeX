from flask import Flask
from flask_login import LoginManager
import os

app = Flask(__name__)
#more config settings here...

from app import routes

