def add_pokemon_to_session(data, session):
    session["pokemon_id"] = data["_id"]
    session["pokemon_name"] = data["name"]
    session["pokemon_height"] = data["height"]
    session["pokemon_weight"] = data["weight"]
    session["pokemon_types"] = data["pokemonType"]
    session["pokemon_img"] = data["sprites"]
    

def add_droped_pokemon(data, session):
    session.update({'dp_id': data["_id"]})
    session["dp_name"] = data["name"]
    session["dp_height"] = data["height"]
    session["dp_weight"] = data["weight"]
    session["dp_types"] = data["pokemonType"]
    session["dp_img"] = data["sprites"]


def update_money_in_session(session, money):
    session.update({'money': money})

    
def remove_pokemon_from_session(session):
    session.pop("pokemon_id", None)
    session.pop("pokemon_name", None)
    session.pop("pokemon_height", None)
    session.pop("pokemon_weight", None)
    session.pop("pokemon_types", None)
    session.pop("pokemon_img", None)


def remove_user_from_session(session):
    session.pop("username", None)
    session.pop("money", None)