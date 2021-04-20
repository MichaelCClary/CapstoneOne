from flask_wtf import FlaskForm
from wtforms.fields import SelectField
from wtforms.fields.html5 import SearchField
from wtforms.validators import DataRequired, Email, Length
from wtforms_alchemy import ModelForm
from models import User, db, Mechanic, Category, connect_db
from wtforms_alchemy import model_form_factory
from flask import Flask
# The variable db here is a SQLAlchemy object instance from
# Flask-SQLAlchemy package

app = Flask(__name__)
app.config.from_object('config.Config')
connect_db(app)

BaseModelForm = model_form_factory(FlaskForm)

mechanic_query = Mechanic.query.all()
mechanic_choices = [(None, "....")]
for mechanic in mechanic_query:
    choice = (mechanic.id, mechanic.name)
    mechanic_choices.append(choice)

category_query = Category.query.all()
category_choices = [(None, "....")]
for category in category_query:
    choice = (category.id, category.name)
    category_choices.append(choice)

searchby_choices = [
    ("", "..."),
    ("name", "Name"),
    ("mechanics", "Mechanic"),
    ("categories", "Category")
]

order_choices = {
    "popularity": "Popularity",
    "name": "Name",
    "name_reverse": "Name Reverse",
    "price": "Price",
    "price_reverse": "Price Reverse",
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
    order_by = SelectField('Order By', choices=[
                          (k, v) for k, v in order_choices.items()])
