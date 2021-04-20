import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get(DATABASE_URL, 'postgresql:///boardgames_db'))
    DEVELOPMENT = True
    SECRET_KEY = os.environ.get('SECRET_KEY', "it's a secret")
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
