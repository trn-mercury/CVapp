"""
Routes and views for the flask application.
"""

from datetime import datetime
from turtle import title
from flask import render_template, request, redirect, url_for
from CVapp import app
from CVapp.projects import Project, Bullet

import sqlite3

def get_db_connection():
    conn = sqlite3.connect('projects.db')
    return conn

def get_project(project_id, c):
    c.execute('SELECT id, title, role, start_date, end_date, description FROM projects WHERE id=?', (project_id,))
    row = c.fetchone()
    if row:
        project_id = row[0]
        title = row[1]
        role = row[2]
        start_date = row[3]
        end_date = row[4]
        description = row[5]
        c.execute('SELECT id, text FROM bullets WHERE project_id=?', (project_id,))
        bullets = [Bullet(bullet_row[0], bullet_row[1]) for bullet_row in c.fetchall()]
        project = Project(project_id, title, role, start_date, end_date, description, bullets)
    else:
        project = None
    return project

def get_projects():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT id, title, role, start_date, end_date, description FROM projects')
    projects = []
    for row in c.fetchall():
        project_id = row[0]
        title = row[1]
        role = row[2]
        start_date = row[3]
        end_date = row[4]
        description = row[5]
        c.execute('SELECT id, text FROM bullets WHERE project_id=?', (project_id,))
        bullets = [Bullet(bullet_row[0], bullet_row[1]) for bullet_row in c.fetchall()]
        projects.append(Project(project_id, title, role, start_date, end_date, description, bullets))
    conn.close()
    return projects


# Starting routing here
@app.route('/')
@app.route('/index')
def index():
    projects = get_projects()
    return render_template('index.html', title='My Projects', projects=projects)

@app.route('/add_project', methods=['POST'])
def add_project():
    # Retrieve project data from form
    title = request.form.get("project_title")
    role = request.form.get("role")
    # TODO: handle date types correctly
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    description = request.form.get("description")
    bullets = request.form.getlist("bullets[]")

    conn = get_db_connection()
    c = conn.cursor()
    
    # Insert project into database
    c.execute('''INSERT INTO projects (title, role, start_date, end_date, description) VALUES (?, ?, ?, ?, ?)''', (title, role, start_date, end_date, description))
    project_id = c.lastrowid
    
    # Insert bullets into database
    for bullet in bullets:
        c.execute('''INSERT INTO bullets (text, project_id) VALUES (?, ?)''', (bullet, project_id))
    
    # Commit changes and redirect to index
    conn.commit()
    return redirect("/")

@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM projects WHERE id = ?', (project_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('projects'))

@app.route('/project_detail/<int:project_id>', methods=['GET', 'POST'])
def project_detail(project_id):
    conn = get_db_connection()
    c = conn.cursor()

    # Get the project details from the database
    project = get_project(project_id, c)

    # Handle POST requests for updating the project attributes
    if request.method == 'POST':
        project_title = request.form['project_title']
        project_role = request.form['project_role']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        description = request.form['description']

        # Update the project in the database
        c.execute('UPDATE projects SET title=?, role=?, start_date=?, end_date=?, description=? WHERE id=?', 
                  (project_title, project_role, start_date, end_date, description, project_id))
        conn.commit()

        # Redirect back to the project detail page
        return redirect(url_for('project_detail', project_id=project_id))

    # Handle POST requests for adding a new bullet
    if request.method == 'POST' and 'add_bullet' in request.form:
        bullet_text = request.form['bullet_text']
        c.execute('INSERT INTO bullets (text, project_id) VALUES (?,?)', (bullet_text, project_id))
        conn.commit()
        return redirect(url_for('project_detail', project_id=project_id))

    # Handle POST requests for deleting a bullet
    if request.method == 'POST' and 'delete_bullet' in request.form:
        bullet_id = request.form['delete_bullet']
        c.execute('DELETE FROM bullets WHERE id=?', (bullet_id,))
        conn.commit()
        return redirect(url_for('project_detail', project_id=project_id))

    # Get the bullets for the project from the database
    # c.execute('SELECT id, text FROM bullets WHERE project_id=?', (project_id,))
    bullets = project.getBullets()

    conn.close()

    return render_template('project_detail.html', title='Project Detail Page', project=project, bullets=bullets)


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
