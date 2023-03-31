"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import CVapp.projects
import CVapp.views
import sqlite3

conn = sqlite3.connect('projects.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS projects
             (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, duration TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS bullets
             (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, project_id INTEGER, FOREIGN KEY(project_id) REFERENCES projects(id))''')
conn.commit()