import os


class Config(object):

    DEVELOPMENT = True
    SECRET_KEY = os.environ.get('SECRET_KEY', "it's a secret")
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
