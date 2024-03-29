from flask_bcrypt import Bcrypt
from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from forms import UserAddForm, LoginForm, UserEditForm, SearchForm, populate_category_choices, populate_mechanic_choices
from models import db, connect_db, User, Game, Collection, Mechanic, Category
from external_routes import search_board_games, update_mechanics, update_categories, add_game_to_db
from helper_functions import get_collection_api_ids, keep_data_searchform

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config.from_pyfile('config.py')
toolbar = DebugToolbarExtension(app)
connect_db(app)

bcrypt = Bcrypt()

update_mechanics()
update_categories()
populate_category_choices()
populate_mechanic_choices()


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
    collection_api_ids = get_collection_api_ids(g.user)
    return render_template('home.html', games=games['games'], collection_api_ids=collection_api_ids)


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

    collection_api_ids = get_collection_api_ids(g.user)

    return render_template('game_detail.html', game=game, collection_api_ids=collection_api_ids)


@app.route('/api/collection/toggle', methods=['POST'])
def toggle_collection():

    if not g.user:
        return jsonify("error")

    response = request.get_json()
    api_id = response.get('id', "")

    game = Game.query.filter(
        Game.api_id == api_id).first()

    if not game:
        game = add_game_to_db(api_id)

    if game in g.user.collection:
        g.user.collection.remove(game)
        db.session.commit()
        return jsonify("removed")
    else:
        g.user.collection.append(game)
        db.session.commit()
        return jsonify("added")


@app.route("/search")
def search():
    search_params = {}
    searched_by = request.args.get('searchby', None)

    search_params[searched_by] = request.args.get(searched_by)
    search_params['order_by'] = request.args.get('order_by', 'popularity')
    search_params['fuzzy_match'] = True

    form = keep_data_searchform(
        searched_by, search_params[searched_by], search_params['order_by'])
    games = search_board_games(search_params)

    collection_api_ids = get_collection_api_ids(g.user)

    return render_template('search.html', games=games['games'], form=form, collection_api_ids=collection_api_ids)
