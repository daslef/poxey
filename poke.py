import requests
import json

def get_pokemon_data(name):
    req = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}/")
    if req.status_code != 200:
        return "Error"

    req_data = req.json()

    pokemon_data = {
        "_id": req_data["id"],
        "name": req_data["name"],
        "height": req_data["height"],
        "weight": req_data["weight"],
        "pokemonType": [el["type"]["name"] for el in req_data["types"]],
        "sprites": req_data["sprites"]["front_default"]
    }

    return pokemon_data


def send_info(data, session):
    session["pokemon_id"] = data["_id"]
    session["pokemon_name"] = data["name"]
    session["pokemon_height"] = data["height"]
    session["pokemon_weight"] = data["weight"]
    session["pokemon_types"] = data["pokemonType"]
    session["pokemon_img"] = data["sprites"]
