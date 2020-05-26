from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from poke import get_pokemon_data, send_info
from model import db, create_app, get_user_by_name, add_user, get_user_history, get_pokemon_by_name, add_user_request
from random import randint

app = create_app()
app.app_context().push()

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
        found_user = get_user_by_name(username)

        if found_user:
            flash("Пользователь с таким именем уже зарегистрирован!")
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
    session.pop("username", None)
    session.pop("pokemon_name", None)
    return redirect(url_for("index"))


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if not session.get("username"):
        return redirect(url_for("index"))
    
    user = get_user_by_name(session["username"])
    user_history = list(get_user_history(user._id))
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
                send_info(pokemon_data, session)
        except:
            user_input = request.form["user_input"].lower()
            pokemon_data = get_pokemon_data(user_input)

            if pokemon_data != "Error":
                send_info(pokemon_data, session)

                found_user = get_user_by_name(session["username"])
                
                add_user_request(found_user._id, pokemon_data["_id"], pokemon_data["name"], pokemon_data["pokemonType"][0], pokemon_data["sprites"])
            else:
                session.pop("pokemon_name", None)

    return render_template("search.html")


@app.route("/history")
def pokemon():
    if not session.get("username"):
        return redirect(url_for("index"))

    found_user = get_user_by_name(session["username"])
    user_history = get_user_history(found_user._id)

    if len(list(user_history)) < 9:
        necessary_pokemons = list(user_history)
    else:
        necessary_pokemons = user_history[len(list(user_history)) - 9:]

    return render_template("history.html", pokemons=necessary_pokemons)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
