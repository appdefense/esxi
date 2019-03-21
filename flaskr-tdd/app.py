# imports
import os
import sqlite3
import json


from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy


# get the folder where this file runs
basedir = os.path.abspath(os.path.dirname(__file__))

# configuration
DATABASE = 'esxi.db'
DEBUG = True
SECRET_KEY = 'my_precious'
USERNAME = 'admin'
PASSWORD = 'admin'

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# database config
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False

# create app
app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

import models


@app.route('/')
def index():
    """Searches the database for entries, then displays them."""
    entries = db.session.query(models.Flaskr)
    return render_template('index.html', entries=entries)


@app.route('/add/host', methods=['POST'])
def add_host():
    """Adds new host to the database."""
    if not session.get('logged_in'):
        abort(401)
    new_entry = models.Flaskr(request.form['host_ip'], request.form['alarming'], request.form['remediation'])
    db.session.add(new_entry)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))

@app.route('/add/process', methods=['POST'])
def add_process():
    """Adds new process to the database."""
    if not session.get('logged_in'):
        abort(401)
    new_entry = models.Process(request.form['cli'], request.form['inbound'], request.form['outbound'], request.form['counter'])
    db.session.add(new_entry)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login/authentication/session management."""
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """User logout/authentication/session management."""
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/delete/<int:post_id>', methods=['GET'])
def delete_entry(post_id):
    """Deletes post from database."""
    result = {'status': 0, 'message': 'Error'}
    try:
        new_id = post_id
        db.session.query(models.Flaskr).filter_by(post_id=new_id).delete()
        db.session.commit()
        result = {'status': 1, 'message': "Post Deleted"}
        flash('The entry was deleted.')
    except Exception as e:
        result = {'status': 0, 'message': repr(e)}
    return jsonify(result)


@app.route('/search/', methods=['GET'])
def search():
    query = request.args.get("query")
    entries = db.session.query(models.Flaskr)
    if query:
        return render_template('search.html', entries=entries, query=query)
    return render_template('search.html')

@app.route('/get/inventory', methods=['GET'])
def get_inventory():
    table_name = 'hosts'
    db_file = 'esxi.db'

    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
    db = conn.cursor()

    rows = db.execute("SELECT * from %s" % table_name).fetchall()

    conn.commit()
    conn.close()

    return json.dumps( [dict(x) for x in rows], indent=4 ) #CREATE JSON

@app.route('/get/process', methods=['GET'])
def get_process():
    table_name = 'process'
    db_file = 'esxi.db'

    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
    db = conn.cursor()

    rows = db.execute("SELECT * from %s" % table_name).fetchall()

    conn.commit()
    conn.close()

    return json.dumps( [dict(x) for x in rows], indent=4 ) #CREATE JSON


def create_db():
    from app import db
    from models import Flaskr
    # create the database and the db table
    db.create_all()

    # commit the changes
    db.session.commit()

if __name__ == '__main__':
    create_db()
    app.run()
