from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from wtforms.fields import StringField, PasswordField, TextField
from sqlalchemy_utils import EmailType, PasswordType

flask_bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        EmailType,
        nullable=False,
        unique=True,
        info={'label': 'Email'}
    )

    username = db.Column(
        db.String,
        nullable=False,
        unique=True,
        info={'label': 'Username'}
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/avatar_default.png",
    )

    bio = db.Column(
        db.Text,
        default=u''
    )

    country = db.Column(
        db.Text,
        default=u'USA'
    )

    password = db.Column(
        db.Text,
        nullable=False,
        info={'label': 'Password', 'form_field_class': PasswordField}
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    collection = db.relationship(
        "Game",
        secondary="collections",
        backref=db.backref('user', lazy='subquery')
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = flask_bcrypt.generate_password_hash(
            password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = flask_bcrypt.check_password_hash(
                user.password, password)
            if is_auth:
                return user

        return False


class Game(db.Model):
    """Game schema"""

    __tablename__ = 'games'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False
    )

    image_url = db.Column(
        db.Text
    )

    description = db.Column(
        db.Text
    )

    faq = db.Column(
        db.Text
    )

    msrp = db.Column(
        db.Text
    )

    api_id = db.Column(
        db.Text,
        unique=True
    )

    max_players = db.Column(
        db.Integer
    )

    min_players = db.Column(
        db.Integer
    )

    max_playtime = db.Column(
        db.Integer
    )

    min_playtime = db.Column(
        db.Integer
    )

    min_age = db.Column(
        db.Integer
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    mechanics = db.relationship(
        "Mechanic",
        secondary="games_mechanics",
        backref=db.backref('game', lazy='subquery')
    )

    categories = db.relationship(
        "Category",
        secondary="games_categories",
        backref=db.backref('game', lazy='subquery')
    )

    def __repr__(self):
        return f"<Game #{self.id}: {self.name}, {self.description}>"


class Rating(db.Model):
    """User Rating of games"""

    __tablename__ = 'ratings'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    game_id = db.Column(
        db.Integer,
        db.ForeignKey('games.id', ondelete='cascade'),
        unique=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    rating = db.Column(
        db.Integer
    )


class Mechanic(db.Model):
    """Game mechanics"""

    __tablename__ = 'mechanics'

    id = db.Column(
        db.Text,
        primary_key=True
    )

    name = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )


games_mechanics = db.Table('games_mechanics',
                           db.Column('mechanic_id',
                                     db.Text,
                                     db.ForeignKey(
                                         'mechanics.id', ondelete='cascade'),
                                     primary_key=True
                                     ),

                           db.Column('game_id',
                                     db.Integer,
                                     db.ForeignKey(
                                         'games.id', ondelete='cascade'),
                                     primary_key=True
                                     ),

                           db.Column('created_at',
                                     db.DateTime,
                                     nullable=False,
                                     default=datetime.utcnow(),
                                     )
                           )


class Category(db.Model):
    """Game categories"""

    __tablename__ = 'categories'

    id = db.Column(
        db.Text,
        primary_key=True
    )

    name = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )


games_categories = db.Table('games_categories',
                            db.Column('category_id',
                                      db.Text,
                                      db.ForeignKey(
                                          'categories.id', ondelete='cascade'),
                                      primary_key=True
                                      ),

                            db.Column('game_id',
                                      db.Integer,
                                      db.ForeignKey(
                                          'games.id', ondelete='cascade'),
                                      primary_key=True
                                      ),

                            db.Column('created_at',
                                      db.DateTime,
                                      nullable=False,
                                      default=datetime.utcnow(),
                                      )
                            )


class Collection(db.Model):
    """User collection of games"""

    __tablename__ = 'collections'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    game_id = db.Column(
        db.Integer,
        db.ForeignKey('games.id', ondelete='cascade')
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    name = db.Column(
        db.Text,
        default="Personal"
    )


def connect_db(app):
    """Connect this database to flask app.
    """

    db.app = app
    db.init_app(app)
