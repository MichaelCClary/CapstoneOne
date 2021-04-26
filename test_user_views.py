"""User views tests."""

# run these tests like:
#
#   flask_env=production python -m unittest test_user_views.py

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


class UserViewsTestCase(TestCase):
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

    def test_sign_up_good(self):
        with app.test_client() as client:
            username = "TestTestTest"
            password = "Wayne123"
            email = "Test@test.com"
            new_user = {"username": username,
                        "password": password, "email": email}

            number_of_users_before = len(User.query.all())

            resp = client.post("/signup", data=new_user,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            user = User.query.filter_by(
                username=username).first()
            number_of_users_after = len(User.query.all())

            self.assertEqual(resp.status_code, 200)
            self.assertTrue(bool(user))
            self.assertIn(
                f"""<p class="title">\n            Welcome to the Vault\n        </p>""", html)
            self.assertEqual(session[CURR_USER_KEY], user.id)
            self.assertNotEqual(number_of_users_after, number_of_users_before)

    def test_sign_up_dupe_username(self):
        with app.test_client() as client:
            username = self.u.username
            password = "Wayne123"
            email = "test@test.com"
            new_user = {"username": username,
                        "password": password, "email": email}

            number_of_users_before = len(User.query.all())

            resp = client.post("/signup", data=new_user,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            db.session.rollback()
            number_of_users_after = len(User.query.all())

            user = User.query.filter_by(
                username=username).first()

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<form", html)
            self.assertEqual(number_of_users_after, number_of_users_before)
            self.assertEqual(user.id, self.u.id)
            self.assertFalse(CURR_USER_KEY in session)

    def test_sign_up_dupe_email(self):
        with app.test_client() as client:
            username = "testuser123"
            password = "Wayne123"
            email = self.u.email
            new_user = {"username": username,
                        "password": password, "email": email}

            number_of_users_before = len(User.query.all())

            resp = client.post("/signup", data=new_user,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            db.session.rollback()
            number_of_users_after = len(User.query.all())

            user = bool(User.query.filter_by(
                username=username).first())

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<form", html)
            self.assertEqual(number_of_users_after, number_of_users_before)
            self.assertFalse(user)
            self.assertFalse(CURR_USER_KEY in session)

    def test_login_good(self):
        with app.test_client() as client:

            returning_user = {"username": self.username,
                              "password": self.password}

            resp = client.post("/login", data=returning_user,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                f"""<p class="title">\n            Welcome to the Vault\n        </p>""", html)
            self.assertEqual(session[CURR_USER_KEY], self.u.id)

    def test_login_bad(self):
        with app.test_client() as client:

            returning_user = {"username": self.u.username,
                              "password": "notpassword"}

            resp = client.post("/login", data=returning_user,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                f"""Invalid credentials.""", html)
            self.assertFalse(CURR_USER_KEY in session)

    def test_logout_route(self):
        with app.test_client() as client:
            resp = client.get("/logout",
                              follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                f"""<p class="title">\n            Welcome to the Vault\n        </p>""", html)
            self.assertFalse(CURR_USER_KEY in session)

    def test_user_details(self):
        with app.test_client() as client:
            game_id = 'TAAifFP590'
            game = add_game_to_db(game_id)
            self.u.collection.append(game)
            db.session.commit()

            resp = client.get(f"/user/{self.u.id}",
                              follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                f"""{self.username}""", html)
            self.assertIn(
                f"""{self.u.collection[0].name}""", html)

    def test_edit_user_good(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u.id
            username = "BobTheBest"
            email = "bob@bob.bob"

            edit_user = {"username": username,
                         "password": self.password, "email": email}

            number_of_users_before = len(User.query.all())

            resp = c.post(f'/user/{self.u.id}/edit', data=edit_user,
                          follow_redirects=True)
            html = resp.get_data(as_text=True)

            user = User.query.get(self.u.id)
            number_of_users_after = len(User.query.all())

            self.assertEqual(resp.status_code, 200)
            self.assertTrue(bool(user))
            self.assertIn(
                f"""<p class="title is-1">\n                        BobTheBest\n""", html)
            self.assertEqual(number_of_users_after, number_of_users_before)
            self.assertEqual(user.username, username)
            self.assertEqual(user.email, email)

    def test_edit_user_bad_password(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u.id
            username = "BobTheBest"
            email = "bob@bob.bob"

            edit_user = {"username": username,
                         "password": "nottherightpassword", "email": email}

            number_of_users_before = len(User.query.all())

            resp = c.post(f'/user/{self.u.id}/edit', data=edit_user,
                          follow_redirects=True)
            html = resp.get_data(as_text=True)

            user = User.query.get(self.u.id)
            number_of_users_after = len(User.query.all())

            self.assertEqual(resp.status_code, 200)
            self.assertTrue(bool(user))
            self.assertEqual(number_of_users_after, number_of_users_before)
            self.assertNotEqual(user.username, username)
            self.assertNotEqual(user.email, email)
