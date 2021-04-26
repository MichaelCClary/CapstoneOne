from flask_wtf import FlaskForm
from wtforms.fields import SelectField, IntegerField
from wtforms.fields.html5 import SearchField
from wtforms.widgets.html5 import NumberInput
from wtforms.validators import DataRequired, Email, Length, Optional
from wtforms_alchemy import ModelForm
from models import User, db, Mechanic, Category, connect_db
from wtforms_alchemy import model_form_factory
from flask import Flask

BaseModelForm = model_form_factory(FlaskForm)

mechanic_choices = [(None, "Choose One")]
category_choices = [(None, "Choose One")]


def populate_mechanic_choices():
    mechanic_query = Mechanic.query.all()
    for mechanic in mechanic_query:
        choice = (mechanic.id, mechanic.name)
        mechanic_choices.append(choice)


def populate_category_choices():
    category_query = Category.query.all()
    for category in category_query:
        choice = (category.id, category.name)
        category_choices.append(choice)


searchby_choices = [
    ("nope", "Choose One"),
    ("name", "Name"),
    ("mechanics", "Mechanic"),
    ("categories", "Category"),
    ("min_players", "Mininum Players"),
    ("max_players", "Maximum Players"),
]

order_choices = {
    "popularity": "Popularity",
    "name": "Name (A-Z)",
    "name_reverse": "Name (Z-A)",
    "price": "Price (Low-High)",
    "price_reverse": "Price (High-Low)",
}


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class UserAddForm(ModelForm):
    """Form for adding users."""
    class Meta:
        model = User
        only = ['username', 'password', 'email']


class UserEditForm(ModelForm):
    """Form for editing users."""
    class Meta:
        model = User


class LoginForm(ModelForm):
    """Login form."""
    class Meta:
        model = User
        only = ['username', 'password']
        unique_validator = None


class SearchForm(FlaskForm):
    """Form for searching api"""
    searchby = SelectField('Search By', choices=searchby_choices)
    name = SearchField('Name')
    mechanics = SelectField('Mechanic', choices=mechanic_choices)
    categories = SelectField('Category', choices=category_choices)
    min_players = IntegerField("Minimum Players", widget=NumberInput(
        min=1, max=20, step=1), validators=[Optional()])
    max_players = IntegerField("Maximum Players", widget=NumberInput(
        min=1, max=20, step=1), validators=[Optional()])
    order_by = SelectField('Order By', choices=[
                          (k, v) for k, v in order_choices.items()])
