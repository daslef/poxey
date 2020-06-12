from datetime import datetime, date
import model

def get_top_pokemons_by_request(requests, result_length):
    popular_pokemons = {}
    
    for req in requests:
        if req.pokemon_name in popular_pokemons.keys():
            popular_pokemons[req.pokemon_name] += 1
        else:
            popular_pokemons.update({req.pokemon_name: 1})
            
    popular_pokemons = sorted(popular_pokemons.items(), key=lambda x: x[1], reverse=True)[:result_length]
    
    return popular_pokemons


def get_top_users_by_request(requests, result_lenght):
    popular_users = {}
    result = {}

    for req in requests:
        if req.user_id in popular_users.keys():
            popular_users[req.user_id] += 1
        else:
            popular_users.update({req.user_id: 1})
    
    for i, k in popular_users.items():
        name = model.get_username_by_id(i)
        result.update({name: k})
    
    result = sorted(result.items(), key=lambda x: x[1], reverse=True)[:result_lenght]
    return result
        

 
def get_last_values(startList, result_length):
    result = []
    
    if len(startList) < result_length:
        result = startList
    else:
        result = startList[len(startList) - result_length:]
        
    return result


def get_date_delta(date):
    current_time = datetime.date(datetime.today())
    days = (current_time - date).days

    return days