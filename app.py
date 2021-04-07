import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

# from forms import UserAddForm, LoginForm, MessageForm, UserEditForm
from models import db, connect_db, User, Game, Collection
from config import Config

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config.from_object('config.Config')
toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def homepage():
    """Show homepage
    """

    return render_template('home.html')
