"""Game views tests."""

# run these tests like:
#
#   flask_env=production python -m unittest test_game_views.py

from unittest import TestCase
from helper_functions import get_collection_api_ids, keep_data_searchform
from external_routes import add_game_to_db, update_categories, update_mechanics
from models import db, User, Game, Collection, Category, Mechanic
from flask import Flask, session
from app import do_login, do_logout, CURR_USER_KEY, add_user_to_g
from sqlalchemy.exc import IntegrityError

from app import app  # nopep8
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///boardgames-test'


# Don't req CSRF for testing
app.config['WTF_CSRF_ENABLED'] = False

db.create_all()


class GameViewsTestCase(TestCase):
    """Test views for user."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Game.query.delete()
        Collection.query.delete()
        Mechanic.query.delete()
        Category.query.delete()
        self.client = app.test_client()

        update_categories()
        update_mechanics()

        self.username = "username123"
        self.password = "Passwordy123"
        self.email = "test123@test.com"

        user_one = User.signup(self.username, self.email,
                               self.password, User.image_url.default.arg)

        db.session.add(user_one)
        db.session.commit()

        self.u = user_one
        self.u.id = user_one.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_game_details(self):
        """ game details page"""
        with app.test_client() as client:
            game_id = 'TAAifFP590'
            game = add_game_to_db(game_id)

            resp = client.get(f"/games/{game_id}",
                              follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                f"""{game.name}""", html)
            self.assertIn(
                f"""{game.description}""", html)
            self.assertIn(
                f"""{game.faq}""", html)

    def test_toggle_collection(self):
        """Toggle, first time adds to collection, 2nd time removes it"""
        url = '/api/collection/toggle'
        id = {'id': 'TAAifFP590'}
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u.id

            resp = c.post(url, json=id)

            self.assertEqual(resp.status_code, 200)

            user = User.query.get(self.u.id)
            data = resp.json

            self.assertEqual(data, 'added')
            self.assertEqual(user.collection[0].api_id, id['id'])

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u.id

            resp = c.post(url, json=id)

            self.assertEqual(resp.status_code, 200)

            user = User.query.get(self.u.id)

            data = resp.json
            self.assertEqual(data, 'removed')
            self.assertEqual(user.collection, [])

    def test_search(self):
        """Search page"""

        # Default search - no query string
        url = "/search"
        with app.test_client() as client:

            resp = client.get(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                f"""<label for="field" class="label">Search By</label>""", html)

        # Search by name, name is dice and order_by popularity
        name = 'lol'
        url = f'search?searchby=name&name={name}&mechanics=None&categories=None&min_players=&max_players=&order_by=popularity'
        with app.test_client() as client:

            resp = client.get(url, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                f"""<label for="field" class="label">Search By</label>""", html)
            self.assertIn(
                f"""{name}""", html.lower())
