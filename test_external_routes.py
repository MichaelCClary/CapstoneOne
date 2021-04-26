"""External Routes functions tests."""

# run these tests like:
#
#   flask_env=production python -m unittest test_external_routes.py


from unittest import TestCase
from external_routes import search_board_games, update_mechanics, update_categories, add_game_to_db
from models import db, User, Game, Collection, Category, Mechanic
from sqlalchemy.exc import IntegrityError


from app import app  # nopep8

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///boardgames-test'

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
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
        name = 'name'
        search_params = {name: 'lol'}
        games = search_board_games(search_params)

        self.assertGreater(len(games), 0)
        self.assertIn(search_params[name], games['games'][0]['name'].lower())

    def test_update_mechanics(self):
        original_mechanics = Mechanic.query.all()

        self.assertEqual(len(original_mechanics), 0)

        update_mechanics()

        updated_mechanics = Mechanic.query.all()

        self.assertGreater(updated_mechanics, original_mechanics)

    def test_update_categories(self):
        original_categories = Category.query.all()

        self.assertEqual(len(original_categories), 0)

        update_categories()

        updated_categories = Category.query.all()

        self.assertGreater(updated_categories, original_categories)

    def test_add_game_to_db(self):
        id = 'TAAifFP590'

        first_game_search = Game.query.filter(
            Game.api_id == id).first()

        self.assertEqual(first_game_search, None)

        added_game = add_game_to_db(id)

        second_game_search = Game.query.filter(
            Game.api_id == id).first()

        print(added_game)

        self.assertEqual(second_game_search, added_game)
        self.assertEqual(second_game_search['api_id'], id)
