import requests
import json
from django.shortcuts import render


def list_pokemons(request):
    request_filtered = request.GET
    limit = request_filtered.get('limit', 10)
    endpoint = 'https://pokeapi.co/api/v2/pokemon/?limit={}'.format(limit)
    poke_res = requests.get(endpoint)
    poke_array = json.loads(poke_res.content)
    pokemons = []
    for poke in poke_array['results']:
        poke_detail_response = requests.get(poke['url'])
        poke_detail_content = poke_detail_response.content
        poke_detail_dict = json.loads(poke_detail_content)
        poke_details = dict(name=poke['name'], url=poke['url'],
                            img=poke_detail_dict['sprites']['front_default'],
                            id=poke_detail_dict['id'])
        pokemons.append(poke_details)
    return render(request, "index.html", {'pokemons': pokemons})


def retrieve_poke(request, id_poke=None):
    url_detail_poke = "https://pokeapi.co/api/v2/pokemon/{}/".format(id_poke)
    poke_res = requests.get(str(url_detail_poke))
    poke_dict = json.loads(poke_res.content)
    types = poke_dict['types']
    formated_types = []
    for type_edit in types:
        id_type = type_edit['type']['url']
        r = id_type.split('/')
        r_last = r[-2]
        formated_types.append(dict(name=type_edit['type']['name'], id=r_last))

    poke_detail = dict(name=poke_dict['name'], img=poke_dict['sprites']['front_default'], weight=poke_dict['weight'],
                       height=poke_dict['height'], types=formated_types,
                       abilities=poke_dict['abilities'], moves=poke_dict['moves'])
    return render(request, "details.html", {'details': poke_detail})


def type_pokes(request, type_poke=None):
    url_type_endpoint = "https://pokeapi.co/api/v2/type/{}/".format(type_poke)
    type_res = requests.get(str(url_type_endpoint))
    type_dict = json.loads(type_res.content)
    pokes_per_type = []
    for pokemon in type_dict['pokemon']:
        id_poke = pokemon['pokemon']['url']
        r = id_poke.split('/')
        id_poke = r[-2]
        pokes_per_type.append(dict(name=pokemon['pokemon']['name'], url=pokemon['pokemon']['url'], id_poke=str(id_poke)))
    return render(request, "type.html", {'pokes_per_type': pokes_per_type})
