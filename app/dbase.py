from app import app
import sqlite3
from flask import g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
    curs = g.db.cursor()
    return curs

def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()