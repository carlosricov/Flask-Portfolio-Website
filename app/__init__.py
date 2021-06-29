from flask import Flask, render_template, url_for, json, Response, request
import os
from . import db
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(os.getcwd(), 'flask.sqlite')
db.init_app(app)

# code by kOssi (https://stackoverflow.com/questions/21133976/flask-load-local-json)
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
SITE_FOLDER = "static/data"

# Homepage
@app.route('/')
def index():
    return render_template('landing_page.html')

# Profiles
@app.route('/profile/<name>')
def profile(name):
    json_url = os.path.join(SITE_ROOT, SITE_FOLDER, f"{name}.json")
    data = json.load(open(json_url))
    return render_template('profile.html', data=data)

# Health Check 
@app.route('/health', methods=["GET"])
def health():
    return Response("Something Here"), 200

# Register endpoint
@app.route('/register', methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.\n'
        elif not password:
            error = 'Password is required.\n'
        elif db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
            error = f"User {username} is already registered.\n"
        
        if error is None:
            db.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, generate_password_hash(password)))
            db.commit()
            return f"User {username} created successfully\n"
        else:
            return error, 418
    
    return "Register Page not yet implemented", 501 

# Login endpoint
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

        if user is None:
            error = 'Incorrect username.\n'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.\n'
        
        if error is None:
            return "Login Successful", 200
        else:
            return error, 418
    
    
    # return "Login Page not yet implemented", 501
    return render_template('login.html')


