import requests
from models import db, connect_db, User, Game, Collection, Mechanic, Category
from secrets import client_id
from flask import Flask

app = Flask(__name__)
app.config.from_object('config.Config')
connect_db(app)


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


def add_game_to_db():
