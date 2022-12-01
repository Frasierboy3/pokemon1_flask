from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from app.models import Pokemon, User, teamTable
from sqlalchemy import select

team = Blueprint('team', __name__, template_folder='team_templates')

@team.route('/capture/<int:pokemon_id>')
def capturePokemon(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    if pokemon:
        current_user.capture(pokemon)
    return redirect(url_for('team.viewCurrentTeam'))

@team.route('/release/<int:pokemon_id>')
def releasePokemon(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    if pokemon:
        current_user.release(pokemon)

    return redirect(url_for('team.viewCurrentTeam'))

@team.route('/teams')
def viewTeams():
    users = User.query.all()
    d = {}
    for u in users:
        if Pokemon.query.join(teamTable).join(User).filter(teamTable.c.user_id == u.user_id).all():
            viewTeams = Pokemon.query.join(teamTable).join(User).filter(teamTable.c.user_id == u.user_id).all()
            d[u.first_name] = viewTeams
    return render_template('other_teams.html', d=d, u=u)

@team.route('/current_team')
def viewCurrentTeam():
    viewTeam = Pokemon.query.join(teamTable).join(User).filter(teamTable.c.user_id == current_user.user_id)
    return render_template('team.html',viewTeam=viewTeam)

@team.route('/battle/<current_user>/<user>')
def battleTime(user, current_user):
    user1 = User.query.filter(User.first_name == user).first()
    user2 = User.query.filter(User.first_name == current_user).first()

    team1 = user1.team.all()
    team2 = user2.team.all()

    health_defense_points1 = 0
    attack_points1 = 0
    health_defense_points2 = 0
    attack_points2 = 0

    for pokemon in team1:
        health_defense_points1 += pokemon.defense
        health_defense_points1 += pokemon.hp
        attack_points1 += pokemon.attack

    for pokemon in team2:
        health_defense_points2 += pokemon.defense
        health_defense_points2 += pokemon.hp
        attack_points2 += pokemon.attack

    overall_points_team1 = health_defense_points1 - attack_points2
    overall_points_team2 = health_defense_points2 - attack_points1

    if overall_points_team1 > overall_points_team2:
        user1.wins += 1
        user2.losses += 1
        user1.saveToDB()
        user2.saveToDB()

    elif overall_points_team1 < overall_points_team2:
        user1.losses += 1
        user2.wins += 1
        user1.saveToDB()
        user2.saveToDB()

    elif overall_points_team1 == overall_points_team2:
        user1.ties += 1
        user2.ties += 1
        user1.saveToDB()
        user2.saveToDB()
    return render_template('battle.html', team1=team1, team2=team2, user1=user1, user2=user2, overall_points_team1=overall_points_team1, overall_points_team2=overall_points_team2)