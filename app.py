from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint
from flask_socketio import SocketIO
from datetime import datetime, date
from model import *
import poke
import session_utils
import utils

app = create_app()
app.app_context().push()
socket = SocketIO(app)


@app.route("/")
def index():
    if session.get("username"):
        return redirect(url_for("search"))

    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if session.get("username"):
        return redirect(url_for("search"))

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        password = generate_password_hash(password)

        if get_user_by_name(username):
            flash("Пользователь с таким именем уже зарегистрирован!")
            return redirect(url_for("signup"))
        elif get_user_by_email(email):
            flash("Пользователь с такой почтой уже зарегистрирован!")
            return redirect(url_for("signup"))
        else:
            add_user(username, email, password)
            session["username"] = username
            user = get_user_by_name(username)
            session_utils.update_money_in_session(session, user.money)
        return redirect(url_for("search"))

    return render_template("signup.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if session.get("username"):
        return redirect(url_for("search"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = get_user_by_name(username)

        if user and check_password_hash(user.password, password):
            session["username"] = username
            session_utils.update_money_in_session(session, user.money)
            return redirect(url_for("search", name=user.name))
        else:
            flash("Неправильный логин или пароль!")

    return render_template("signin.html")


@app.route("/logout")
def logout():
    session_utils.remove_user_from_session(session)
    session_utils.remove_pokemon_from_session(session)
    return redirect(url_for("index"))


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if not session.get("username"):
        return redirect(url_for("index"))

    if request.method == "POST":
        new_user_name = request.form["new_name"]
        if not get_user_by_name(new_user_name):    
            change_user_name(session["username"], new_user_name)
            session_utils.remove_user_from_session(session)
            return redirect(url_for("signin"))
        else:
            flash("Данный логин уже занят!")
        
    user = get_user_by_name(session["username"])
    user_history = get_user_history(user._id)
    pokemons_count = {}

    registrered_time = user.registered_on
    current_time = datetime.date(datetime.today())
    days = (current_time-registrered_time).days

    
    for req in user_history:
        if req.pokemon_name not in pokemons_count.keys():
            pokemons_count.update({req.pokemon_name: 1})
        else:
            pokemons_count[req.pokemon_name] += 1
    
    popular_pokemon = None
    popular_img = None

    if user_history:
        popular_pokemon = sorted(pokemons_count.items(), key=lambda x: x[1], reverse=True)[0][0]
        popular_img = get_pokemon_by_name(popular_pokemon).pokemon_img

    user_data = {
        "id": user._id,
        "username": user.name,
        "email": user.email,
        "count": len(user_history),
        "pokemon": popular_pokemon,
        "img": popular_img,
        "days": days
    }
    if get_user_by_name(session["username"]).is_admin:
        return render_template("profile.html", user_data=user_data, admin=True)
    else:
        return render_template("profile.html", user_data=user_data)


@app.route("/search", methods=["GET", "POST"])
def search():
    if not session.get("username"):
        return redirect(url_for("index"))

    if request.method == "POST":
        try:
            if request.form["random_button"]:
                pokemon_data = poke.get_pokemon_data(randint(1, 807))
                session_utils.add_pokemon_to_session(pokemon_data, session)
        except:
            user_input = request.form["user_input"].lower()
            pokemon_data = poke.get_pokemon_data(user_input)

            if pokemon_data != "Error":
                session_utils.add_pokemon_to_session(pokemon_data, session)

                found_user = get_user_by_name(session["username"])

                add_user_request(found_user._id, pokemon_data["_id"], pokemon_data["name"],
                                 pokemon_data["pokemonType"][0], pokemon_data["sprites"])
                add_money(found_user, randint(1, 10))
                
                session_utils.update_money_in_session(session, found_user.money)
                
            else:
                session.pop("pokemon_name", None)

    return render_template("search.html")


@app.route("/history")
def history():
    if not session.get("username"):
        return redirect(url_for("index"))

    found_user = get_user_by_name(session["username"])
    user_history = get_user_history(found_user._id)
    necessary_pokemons = utils.get_last_values(user_history, 9)[::-1]

    return render_template("history.html", pokemons=necessary_pokemons)


@app.route("/rating")
def rating():
    if not session.get("username"):
        return redirect(url_for("index"))
    
    users_requests = get_all_users_request()
    popular_pokemons = utils.get_top_pokemons_by_request(users_requests, 5)
    
    return render_template("rating.html", popular_pokemons=popular_pokemons)


@app.route("/admin")
def admin_panel():
    if not session.get("username"):
        return redirect(url_for("index"))

    found_user = get_user_by_name(session["username"])

    if not found_user.is_admin:
        return redirect(url_for("search"))

    return render_template("adminPanel.html")


@app.route("/chat")
def chat():
    if not session.get("username"):
        return redirect(url_for("index"))

    messages = get_all_messages()
    necessary_messages = utils.get_last_values(messages, 100)

    return render_template("chat.html", messages=necessary_messages)


@app.route("/process_data/", methods=["POST"])
def test():
    if not session.get("username"):
        return redirect(url_for("index"))

    found_user = get_user_by_name(session["username"])

    if not found_user.is_admin:
        return redirect(url_for("search"))

    return render_template("adminPanel.html")


@socket.on("userMessage")
def handle_user_message(json, methods=["GET", "POST"]):
    timestamp = f"{datetime.now().hour:02}:{datetime.now().minute:02}"

    add_message(json["username"], json["message"], datetime.now())

    json.update({"time": timestamp})
    socket.emit("messageResponse", json)


if __name__ == "__main__":
    db.create_all()
    socket.run(app, debug=True)
