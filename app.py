from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from poke import get_pokemon_data, send_info
from random import randint

app = Flask(__name__)
app.secret_key = '*PInefdlyv5@'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(hours=1)

db = SQLAlchemy(app)


class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    user_requests = db.relationship('UserRequests', backref='user', lazy=True)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __str__(self):
        return f"Username - {self.name} Email - {self.email}"


class UserRequests(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pokemon_id = db.Column(db.Integer)
    pokemon_name = db.Column(db.String(60))
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


@app.route('/')
def index():
    if session.get('username'):
        return redirect(url_for("search"))
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if session.get('username'):
        return redirect(url_for("search"))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password = generate_password_hash(password)
        found_user = User.query.filter_by(name=username).first()

        if found_user:
            flash("Пользователь с таким именем уже зарегистрирован!")
            return redirect(url_for("signup"))
        else:
            user = User(username, email, password)
            db.session.add(user)
            db.session.commit()
            session['username'] = username
        return redirect(url_for("search"))

    return render_template("signup.html")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if session.get('username'):
        return redirect(url_for("search"))

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(name=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('search', name=user.name))
        else:
            flash("Неправильный логин или пароль!")

    return render_template("signin.html")


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('pokemon_name', None)
    return redirect(url_for("index"))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('username'):
        return redirect(url_for("index"))
    
    user = User.query.filter_by(name=session['username']).first()
    user_history = list(UserRequests.query.filter_by(user_id=user._id))
    pokemons_count = {}

    for req in user_history:
        if req.pokemon_name not in pokemons_count.keys():
            pokemons_count.update({req.pokemon_name: 1})
        else:
            pokemons_count[req.pokemon_name] += 1

    popular_pokemon = sorted(pokemons_count.items(), key=lambda x: x[1], reverse=True)[0][0]
    popular_img = UserRequests.query.filter_by(pokemon_name=popular_pokemon).first().pokemon_img
    user_data = {
        "id": user._id,
        "username": user.name, 
        "email": user.email, 
        "count": len(user_history),
        "pokemon": popular_pokemon, 
        "img": popular_img
    }

    return render_template("profile.html", user_data=user_data)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if not session.get('username'):
        return redirect(url_for("index"))

    if request.method == "POST":
        try:
            if request.form['random_button']:
                pokemon_data = get_pokemon_data(randint(1, 807))
                send_info(pokemon_data, session)
        except:
            user_input = request.form["user_input"].lower()
            pokemon_data = get_pokemon_data(user_input)

            if pokemon_data != "Error":
                send_info(pokemon_data, session)

                found_user = User.query.filter_by(name=session['username']).first()

                user_req = UserRequests(found_user._id, pokemon_data["_id"], pokemon_data["name"], pokemon_data["pokemonType"][0], pokemon_data["sprites"])
                db.session.add(user_req)
                db.session.commit()
            else:
                session.pop('pokemon_name', None)

    return render_template("search.html")


@app.route('/history')
def pokemon():
    if not session.get('username'):
        return redirect(url_for("index"))

    found_user = User.query.filter_by(name=session['username']).first()
    user_history = UserRequests.query.filter_by(user_id=found_user._id)

    if len(list(user_history)) < 9:
        necessary_pokemons = list(user_history)
    else:
        necessary_pokemons = user_history[len(list(user_history)) - 9:]

    return render_template("history.html", pokemons=necessary_pokemons)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
