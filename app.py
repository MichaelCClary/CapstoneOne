from flask_bcrypt import Bcrypt
import os

from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from wtforms_alchemy import ModelForm
from forms import UserAddForm, LoginForm, UserEditForm, SearchForm
from models import db, connect_db, User, Game, Collection, Mechanic, Category
from config import Config
from external_routes import search_board_games, update_mechanics, update_categories, add_game_to_db

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config.from_object('config.Config')
toolbar = DebugToolbarExtension(app)

connect_db(app)

bcrypt = Bcrypt()

update_mechanics()
update_categories()


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/')
def homepage():
    """Show homepage
    """
    games = search_board_games()
    ids = get_collection_ids(g.user)
    return render_template('home.html', games=games['games'], ids=ids)


@app.route('/signup', methods=["GET", "POST"])
def sign_up():
    """Sign up new user"""
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=User.image_url.default.arg
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('/signup.html', form=form)

        do_login(user)

        return redirect("/")
    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def log_in():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout', methods=["GET"])
def log_out():
    do_logout()
    return redirect("/")


@app.route('/user/<int:user_id>')
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)


@app.route('/user/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    """Edit User"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = UserEditForm(obj=g.user)

    if form.validate_on_submit():
        password = form.password.data

        user = User.authenticate(g.user.username, password)
        if user:
            user.username = form.username.data
            user.email = form.email.data
            user.bio = form.bio.data
            user.image_url = form.image_url.data
            user.country = form.country.data

            db.session.commit()
            flash("User Updated", "success")
            do_logout()
            do_login(user)
            return redirect(f"/user/{user.id}")
        else:
            flash("Wrong Password", "danger")
            return redirect("/")

    return render_template("edit_user.html", form=form)


@app.route('/games/<id>')
def game_details(id):
    """Show a single game details"""
    game = Game.query.filter(
        Game.api_id == id).first()

    if not game:
        game = add_game_to_db(id)

    ids = get_collection_ids(g.user)

    return render_template('game_detail.html', game=game, ids=ids)


@app.route('/api/collection/add', methods=['POST'])
def add_to_collection():

    if not g.user:
        return jsonify("error")

    content = request.get_json()
    api_id = content.get('id', "")

    game = Game.query.filter(
        Game.api_id == api_id).first()

    if not game:
        game = add_game_to_db(api_id)

    g.user.collection.append(game)
    db.session.commit()
    return jsonify("added")


@app.route("/search")
def search():
    form = SearchForm()
    search_params = {}
    searchby = request.args.get('searchby', None)
    if searchby:
        search_params[searchby] = request.args.get(searchby)
    else:
        search_params['name'] = request.args.get('name')

    search_params['fuzzy_match'] = True
    print(search_params, flush=True)
    games = search_board_games(search_params)

    return render_template('search.html', games=games['games'], form=form)


def get_collection_ids(user):
    ids = []
    if user:
        for game in user.collection:
            ids.append(game.api_id)

    return ids
