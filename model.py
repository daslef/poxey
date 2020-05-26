from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, date

db = SQLAlchemy()


class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_requests = db.relationship("UserRequests", backref="user", lazy=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
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
    return UserRequests.query.filter_by(user_id=user_id)


def get_pokemon_by_name(pokemon_name):
    return UserRequests.query.filter_by(pokemon_name=pokemon_name).first()


def add_user(username, email, password):
    user = User(username, email, password)
    db.session.add(user)
    db.session.commit()


def add_user_request(user_id, pokemon_id, pokemon_name, pokemon_type, pokemon_img):
    user_req = UserRequests(user_id, pokemon_id, pokemon_name, pokemon_type, pokemon_img)
    db.session.add(user_req)
    db.session.commit()


def get_all_users():
    return User.query.all()
    

def make_user_admin(user):
    user.is_admin = True
    db.session.commit()