def get_top_pokemons_by_request(request, result_length):
    popular_pokemons = {}
    
    for req in request:
        if req.pokemon_name in popular_pokemons.keys():
            popular_pokemons[req.pokemon_name] += 1
        else:
            popular_pokemons.update({req.pokemon_name: 1})
            
    popular_pokemons = sorted(popular_pokemons.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return popular_pokemons