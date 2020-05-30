from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, date, datetime

db = SQLAlchemy()


class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_requests = db.relationship("UserRequests", backref="user", lazy=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_banned = db.Column(db.Boolean, default=False, nullable=False)
    registered_on = db.Column(db.Date, default=date.today())


    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


    def __str__(self):
        return f"Username - {self.name} Email - {self.email}"


class UserRequests(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    pokemon_id = db.Column(db.Integer, nullable=False)
    pokemon_name = db.Column(db.String(60), nullable=False)
    pokemon_type = db.Column(db.String(20))
    pokemon_img = db.Column(db.String(400))


    def __init__(self, user_id, pokemon_id, pokemon_name, pokemon_type, pokemon_img):
        self.user_id = user_id
        self.pokemon_id = pokemon_id
        self.pokemon_name = pokemon_name
        self.pokemon_type = pokemon_type
        self.pokemon_img = pokemon_img


    def __str__(self):
        return f"UserID - {self.user_id} Pokemon - {self.pokemon_name}"


class ChatHistory(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(20), nullable=False)
    message = db.Column("message", db.String(200), nullable=False)
    sent_on = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, username, message, sent_on):
        self.username = username
        self.message = message
        self.sent_on = sent_on


def create_app():
    app = Flask(__name__)
    app.secret_key = "*PInefdlyv5@"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.permanent_session_lifetime = timedelta(hours=1)
    db.init_app(app)
    return app


def get_user_by_name(name):
    return User.query.filter_by(name=name).first()


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_history(user_id):
    return list(UserRequests.query.filter_by(user_id=user_id))


def get_pokemon_by_name(pokemon_name):
    return UserRequests.query.filter_by(pokemon_name=pokemon_name).first()
    

def change_user_name(old_name, new_name):
    user = get_user_by_name(old_name)
    user.name = new_name
    db.session.commit()
    

def get_all_banned_users():
    return list(User.query.filter_by(is_banned=True))


def get_all_users():
    return list(User.query.all())
    
    
def get_all_messages():
    return list(ChatHistory.query.all())
    

def check_exist_user_by_name(name):
    user = get_user_by_name(name)
    
    if user:
        return True
    else:
        return False
        

def check_exist_user_by_email(email):
    user = get_user_by_email(email)
    
    if user:
        return True
    else:
        return False
    

def add_message(username, message, sent_on):
    user_msg = ChatHistory(username, message, sent_on)
    db.session.add(user_msg)
    db.session.commit()


def add_user(username, email, password):
    user = User(username, email, password)
    db.session.add(user)
    db.session.commit()


def add_user_request(user_id, pokemon_id, pokemon_name, pokemon_type, pokemon_img):
    user_req = UserRequests(user_id, pokemon_id, pokemon_name, pokemon_type, pokemon_img)
    db.session.add(user_req)
    db.session.commit()
    

def make_user_admin(user):
    user.is_admin = True
    db.session.commit()
    

def unmake_user_admin(user):
    user.is_admin = False
    db.session.commit()
    

def ban_user(user):
    user.is_banned = True
    db.session.commit()
    
    
def unban_user(user):
    user.is_banned = False
    db.session.commit()
