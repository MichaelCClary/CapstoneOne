from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from wtforms_alchemy import ModelForm
from models import User, db
from wtforms_alchemy import model_form_factory
# The variable db here is a SQLAlchemy object instance from
# Flask-SQLAlchemy package

BaseModelForm = model_form_factory(FlaskForm)


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
