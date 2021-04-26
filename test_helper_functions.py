"""helper functions tests."""

# run these tests like:
#
#   flask_env=production python -m unittest test_helper_functions.py


from unittest import TestCase
from helper_functions import get_collection_api_ids, keep_data_searchform
from models import db, User, Game, Collection, Category, Mechanic
from forms import SearchForm


from app import app  # nopep8

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///boardgames-test'

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
db.create_all()


class HelperFunctionsTestCase(TestCase):
    """Test Helper Functions"""

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

    def test_get_collection_api_ids(self):
        """should get all api_ids from user.collection"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)

        g = Game(
            name='TestGame',
            api_id='12345'
        )

        db.session.add(g)
        u.collection.append(g)
        db.session.commit()

        ids = get_collection_api_ids(u)

        self.assertEqual(len(ids), 1)
        self.assertIn(g.api_id, ids)
