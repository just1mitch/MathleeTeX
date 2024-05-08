import os
import sqlite3

def reset_database():
    if os.path.exists('database.db'):
        os.remove('database.db')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    with open('db_create.sql', 'r') as sql_file:
        sql_script = sql_file.read()
        cursor.executescript(sql_script)
    conn.commit()
    conn.close()

reset_database()
