from turtle import home
from app import app
from flask import render_template, redirect, url_for, request 
import requests as r 
from app.forms import GetPokemon

pokemoninfo = {}
@app.route('/', methods=["GET","POST"])
def homePage():
    form = GetPokemon()
    if request.method == 'POST':
        if form.validate():
            entry = form.pokemon.data 
            response = r.get(f'https://pokeapi.co/api/v2/pokemon/{entry}')
            pokedex = {}
            if response.ok:
                 data = response.json()
                 pokedex = data
                 for entry in pokedex:
                    id = pokedex['id']
                    pokemoninfo['id'] = id
                    name = pokedex['name'] = data ['forms'][0]['name']
                    pokemoninfo['name'] = name
                    ability = pokedex['ability'] = data['abilities'][0]['ability']['name']
                    pokemoninfo['ability'] = ability
                    base_exp = pokedex['base_experience'] = data['base_experience']
                    pokemoninfo['base_exp'] = base_exp
                    sprite = pokedex['front_shiny'] = data['sprites']['front_shiny']
                    pokemoninfo['sprite'] = sprite
                    attack = pokedex['base_stat'] = data['stats'][1]['base_stat']
                    pokemoninfo['attack'] = attack
                    hp = pokedex['base_stat'] = data['stats'][0]['base_stat']
                    pokemoninfo['hp'] = hp
                    defense = pokedex['base_stat'] = data['stats'][2]['base_stat']
                    pokemoninfo['defense']  = defense
                    return redirect(url_for('pokemoncard'))


    return render_template('index.html', form=form )

@app.route('/PokemonCard')
def pokemoncard():
    return render_template('pokemoncard.html', pokemoninfo=pokemoninfo)

