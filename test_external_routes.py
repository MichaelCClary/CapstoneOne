"""External Routes functions tests."""

# run these tests like:
#
#   flask_env=production python -m unittest test_external_routes.py


from unittest import TestCase
from external_routes import search_board_games, update_mechanics, update_categories, add_game_to_db
from models import db, User, Game, Collection, Category, Mechanic
from sqlalchemy.exc import IntegrityError
import sys

from app import app  # nopep8

# checks if database is test database
if app.config['SQLALCHEMY_DATABASE_URI'] != 'postgresql:///boardgames-test':
    print('Wrong database, BAD BAD BAD - use boardgames-test')
    print('source .env-test')
    sys.exit(1)


db.create_all()


class ExternalRoutesTestCase(TestCase):
    """Test External Routes functions."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Game.query.delete()
        Collection.query.delete()
        Mechanic.query.delete()
        Category.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_search_board_games(self):
        """Searches API using arguments sent to function"""
        name = 'name'
        search_params = {name: 'lol'}
        games = search_board_games(search_params)

        self.assertGreater(len(games), 0)
        self.assertIn(search_params[name], games['games'][0]['name'].lower())

    def test_update_mechanics(self):
        """Updates mechanics in database from api"""
        predicted_response = 'good_update'
        original_mechanics = Mechanic.query.all()

        actual_response = update_mechanics()

        updated_mechanics = Mechanic.query.all()

        self.assertEqual(len(original_mechanics), 0)
        self.assertEqual(actual_response, predicted_response)
        self.assertGreater(len(updated_mechanics), len(original_mechanics))

    def test_update_categories(self):
        """Updates categories in database from api"""
        predicted_response = 'good_update'
        original_categories = Category.query.all()

        actual_response = update_categories()

        updated_categories = Category.query.all()

        self.assertEqual(len(original_categories), 0)
        self.assertEqual(actual_response, predicted_response)
        self.assertGreater(len(updated_categories), len(original_categories))

    def test_add_game_to_db(self):
        """using the api id of a game, adds game to database and returns it, if game already in database, just returns it"""
        id = 'TAAifFP590'
        update_categories()
        update_mechanics()

        first_query_all = Game.query.all()
        first_game_search = Game.query.filter(
            Game.api_id == id).first()

        added_game = add_game_to_db(id)

        second_query_all = Game.query.all()
        second_game_search = Game.query.filter(
            Game.api_id == id).first()

        self.assertEqual(first_game_search, None)
        self.assertEqual(len(first_query_all), 0)
        self.assertEqual(second_game_search, added_game)
        self.assertEqual(second_game_search.api_id, id)
        self.assertEqual(len(second_query_all), 1)

    def test_add_game_to_db_duplicate_game(self):
        id = 'TAAifFP590'

        add_game = add_game_to_db(id)

        query_all = Game.query.all()

        db.session.close()
        add_game_again = add_game_to_db(id)

        query_all_again = Game.query.all()

        self.assertEqual(len(query_all), len(query_all_again))
        self.assertEqual(add_game.name, add_game_again.name)

    def test_add_game_to_db_not_a_game(self):
        id = 'ImnotagameIPromise'

        add_game = add_game_to_db(id)

        self.assertEqual(add_game, 'bad_response')
