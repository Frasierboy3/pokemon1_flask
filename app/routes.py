from app import app
from flask import render_template, redirect, url_for, request 
from flask_login import current_user
import requests as r 
from app.forms import GetPokemon
from app.models import Pokemon

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
                    try: 
                        ability2 = pokedex['abilities'][1]['ability']['name'].title()
                        pokemoninfo['ability2'] = ability2
                    except:
                        pass
                    base_exp = pokedex['base_experience'] = data['base_experience']
                    pokemoninfo['base_exp'] = base_exp
                    sprite = pokedex['sprite'] = data['sprites']['front_shiny']
                    pokemoninfo['sprite'] = sprite
                    attack = pokedex['base_stat'] = data['stats'][1]['base_stat']
                    pokemoninfo['attack'] = attack
                    hp = pokedex['base_stat'] = data['stats'][0]['base_stat']
                    pokemoninfo['hp'] = hp
                    defense = pokedex['base_stat'] = data['stats'][2]['base_stat']
                    pokemoninfo['defense']  = defense

                    pokemon_id = pokemoninfo['id']
                    sprite = pokemoninfo['front_shiny']
                    name = pokemoninfo['name']
                    ability = pokemoninfo['ability']
                    attack = pokemoninfo['attack']
                    hp = pokemoninfo['hp']
                    defense = pokemoninfo['defense']

                    new_pokemon = Pokemon.query.filter_by(pokemon_id=pokemon_id).first()
                    if new_pokemon:
                        return redirect(url_for('PokemonCard')) 

                    else:
                        pokemon = Pokemon(pokemon_id, sprite, name, ability, attack, hp, defense)
                        pokemon.saveToDB()
                        return redirect(url_for('PokemonCard')) 


    return render_template('index.html', form=form )

@app.route('/PokemonCard')
def pokemoncard():
    pokemon = Pokemon.query.all()

    catch = set()
    if current_user.is_authenticated:
        current_team = current_user.team.all()
        for p in current_team:
            catch.add(p.pokemon_id)
    return render_template('pokemoncard.html', pokemoninfo=pokemoninfo, pokemon=pokemon,catch=catch )

