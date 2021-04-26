import requests
import os
from models import db, connect_db, User, Game, Collection, Mechanic, Category
from flask import Flask
from secrets import client_id

client_id = os.environ.get('client_id', client_id)


def search_board_games(data={}, type="search"):
    url = f'https://api.boardgameatlas.com/api/{type}?'
    data['client_id'] = client_id
    response = requests.get(url, params=data).json()
    return response


def update_mechanics():
    mechanics = search_board_games(type="game/mechanics")
    for mechanic in mechanics['mechanics']:
        check_for_id = Mechanic.query.filter(
            Mechanic.id == mechanic['id']).all()
        if len(check_for_id) < 1:
            m = Mechanic(id=mechanic['id'], name=mechanic['name'])
            db.session.add(m)
            db.session.commit()

    db.session.close()


def update_categories():
    categories = search_board_games(type="game/categories")
    for category in categories['categories']:
        check_for_id = Category.query.filter(
            Category.id == category['id']).all()
        if len(check_for_id) < 1:
            m = Category(id=category['id'], name=category['name'])
            db.session.add(m)
            db.session.commit()

    db.session.close()


def add_game_to_db(id):
    params = {'ids': id}
    game = search_board_games(params)['games'][0]
    try:
        new_game = Game(
            api_id=game['id'],
            name=game['name'],
            msrp=game['msrp'],
            description=game['description'],
            faq=game['faq'],
            min_age=game['min_age'],
            min_players=game['min_players'],
            max_players=game['max_players'],
            min_playtime=game['min_playtime'],
            max_playtime=game['max_playtime'],
            image_url=game['image_url']
        )
        db.session.add(new_game)

        for mechanic in game['mechanics']:
            m = Mechanic.query.filter(
                Mechanic.id == mechanic['id']).first()
            new_game.mechanics.append(m)

        for category in game['categories']:
            c = Category.query.filter(
                Category.id == category['id']).first()
            new_game.categories.append(c)

        db.session.commit()
        return new_game
    except:
        db.session.close()
        game = Game.query.filter(
            Game.api_id == game['id']).first()
        return game
