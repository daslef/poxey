from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from poke import get_pokemon_data
from session_utils import add_pokemon_to_session, remove_pokemon_from_session, remove_user_from_session
from model import *
from random import randint
from flask_socketio import SocketIO
from datetime import datetime

app = create_app()
app.app_context().push()

socketio = SocketIO(app)

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
            return redirect(url_for("search", name=user.name))
        else:
            flash("Неправильный логин или пароль!")

    return render_template("signin.html")


@app.route("/logout")
def logout():
    remove_user_from_session(session)
    remove_pokemon_from_session(session)
    return redirect(url_for("index"))


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if not session.get("username"):
        return redirect(url_for("index"))
    
    user = get_user_by_name(session["username"])
    user_history = get_user_history(user._id)
    pokemons_count = {}

    for req in user_history:
        if req.pokemon_name not in pokemons_count.keys():
            pokemons_count.update({req.pokemon_name: 1})
        else:
            pokemons_count[req.pokemon_name] += 1

    popular_pokemon = sorted(pokemons_count.items(), key=lambda x: x[1], reverse=True)[0][0]
    popular_img = get_pokemon_by_name(popular_pokemon).pokemon_img
    
    user_data = {
        "id": user._id,
        "username": user.name, 
        "email": user.email, 
        "count": len(user_history),
        "pokemon": popular_pokemon, 
        "img": popular_img
    }

    return render_template("profile.html", user_data=user_data)


@app.route("/search", methods=["GET", "POST"])
def search():
    if not session.get("username"):
        return redirect(url_for("index"))

    if request.method == "POST":
        try:
            if request.form["random_button"]:
                pokemon_data = get_pokemon_data(randint(1, 807))
                add_pokemon_to_session(pokemon_data, session)
        except:
            user_input = request.form["user_input"].lower()
            pokemon_data = get_pokemon_data(user_input)

            if pokemon_data != "Error":
                add_pokemon_to_session(pokemon_data, session)

                found_user = get_user_by_name(session["username"])
                
                add_user_request(found_user._id, pokemon_data["_id"], pokemon_data["name"], pokemon_data["pokemonType"][0], pokemon_data["sprites"])
            else:
                session.pop("pokemon_name", None)

    return render_template("search.html")


@app.route("/history")
def history():
    if not session.get("username"):
        return redirect(url_for("index"))

    found_user = get_user_by_name(session["username"])
    user_history = get_user_history(found_user._id)

    if len(user_history) < 9:
        necessary_pokemons = user_history
    else:
        necessary_pokemons = user_history[len(user_history) - 9:]

    return render_template("history.html", pokemons=necessary_pokemons)
    
@app.route("/rating")
def rating():
    if not session.get("username"):
        return redirect(url_for("index"))
        
    return render_template("rating.html")

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
    
    if len(messages) < 100:
        necessary_messages = messages
    else:
        necessary_messages = messages[len(messages) - 100:]
    
    return render_template("chat.html", messages=necessary_messages)
        

@app.route("/process_data/", methods=["POST"])  
def test():
    if not session.get("username"):
        return redirect(url_for("index"))
        
    found_user = get_user_by_name(session["username"])
    
    if not found_user.is_admin:
        return redirect(url_for("search"))
    
    
    return render_template("adminPanel.html")
    
    
@socketio.on("userMessage")
def handle_user_message(json, methods=["GET", "POST"]):
    timestamp = f"{datetime.now().hour:02}:{datetime.now().minute:02}"
    
    add_message(json["username"], json["message"], datetime.now())
    
    json.update({"time": timestamp})
    socketio.emit("messageResponse", json)


if __name__ == "__main__":
    db.create_all()
    socketio.run(app, debug=True)
