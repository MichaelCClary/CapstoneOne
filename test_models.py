"""All model tests."""

# run these tests like:
#
#   flask_env=production python -m unittest test_models.py


from unittest import TestCase
from models import db, User, Game, Collection, Category, Mechanic
from sqlalchemy.exc import IntegrityError
import sys


from app import app  # nopep8

# checks if database is test database
if app.config['SQLALCHEMY_DATABASE_URI'] != 'postgresql:///boardgames-test':
    print('Wrong database, BAD BAD BAD - use boardgames-test')
    print('source .env-test')
    sys.exit(1)

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
db.create_all()


class UserModelTestCase(TestCase):
    """Test all models."""

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

    def test_mechanic_model(self):
        """test mechanic model"""
        original_mechanics = Mechanic.query.all()

        m = Mechanic(
            id='5sdsfd',
            name='Railroad'
        )

        db.session.add(m)
        db.session.commit()

        after_mechanics = Mechanic.query.all()

        self.assertEqual(len(after_mechanics), 1)
        self.assertEqual(len(original_mechanics), 0)

    def test_category_model(self):
        """test category model"""

        original_categorys = Category.query.all()

        c = Category(
            id='5sdsfd',
            name='Charlie'
        )

        db.session.add(c)
        db.session.commit()

        after_categorys = Category.query.all()

        self.assertEqual(len(after_categorys), 1)
        self.assertEqual(len(original_categorys), 0)

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no games in collection
        self.assertEqual(len(u.collection), 0)
        self.assertEqual(f'{u}', f'<User #{u.id}: {u.username}, {u.email}>')

        g = Game(
            name='TestGame'
        )

        db.session.add(g)
        u.collection.append(g)
        db.session.commit()

        self.assertEqual(len(u.collection), 1)

        u.collection.remove(g)
        db.session.commit()

        self.assertEqual(len(u.collection), 0)

    def test_user_signup(self):
        """Test user signup"""

        user_one = User.signup("testuser5", "test5@test.com",
                               "HASHED_PASSWORD", User.image_url.default.arg)

        db.session.add(user_one)
        db.session.commit()

        self.assertIsInstance(user_one, User)
        # Check duplicate email fails
        dupe_email = User.signup("testuser", "test5@test.com",
                                 "HASHED_PASSWORD", User.image_url.default.arg)

        db.session.add(dupe_email)
        with self.assertRaises(IntegrityError):
            db.session.commit()

        db.session.rollback()
        # check duplicate user fails
        dupe_user = User.signup("testuser5", "test36@test.com",
                                "HASHED_PASSWORD", User.image_url.default.arg)

        db.session.add(dupe_user)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_user_authenticate(self):
        """Test user authenticate"""
        username = "TestUser"
        pw = "Password"

        user_one = User.signup(username, "test5@test.com",
                               pw, User.image_url.default.arg)

        db.session.add(user_one)
        db.session.commit()

        self.assertIsInstance(user_one, User)
        self.assertEqual(user_one, User.authenticate(username, pw))
        self.assertFalse(User.authenticate("Testuser", pw))
        self.assertFalse(User.authenticate(username, "password"))

    def test_game_model(self):
        """Test game model"""
        description = '123123123'
        g = Game(
            name='TestGame',
            description=description
        )

        c = Category(
            id='abcde',
            name='Charlie'
        )

        m = Mechanic(
            id='12345',
            name='Railroad'
        )

        db.session.add(g)
        g.mechanics.append(m)
        g.categories.append(c)
        db.session.commit()

        self.assertEqual(g.mechanics[0].name, m.name)
        self.assertEqual(g.categories[0].name, c.name)
        self.assertEqual(f'{g}', f'<Game #{g.id}: {g.name}, {g.description}>')
