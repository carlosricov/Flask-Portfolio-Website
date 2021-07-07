import os
from flask import Flask, render_template, url_for, json, Response, request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from app.db import get_db
# from . import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}'.format(
    user=os.getenv('POSTGRES_USER'),
    passwd=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port=5432,
    table=os.getenv('POSTGRES_DB'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class UserModel(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(), primary_key = True)
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f"<User {self.username}>"

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
        error = None

        if not username:
            error = 'Username is required.\n'
        elif not password:
            error = 'Password is required.\n'
        elif UserModel.query.filter_by(username=username).first() is not None:
            error = f"User {username} is already registered.\n"
        
        if error is None:
            new_user = UserModel(username, generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return f"User {username} created successfully\n"
        else:
            return error, 418
    
    #return "Register Page not yet implemented", 501 
    return render_template('register.html')

# Login endpoint
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None
        user = UserModel.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username.\n'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.\n'
        
        if error is None:
            return "Login Successful", 200
        else:
            return error, 418
    
    
    # return "Login Page not yet implemented", 501
    return render_template('login.html')


