import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "")
DEVELOPMENT = True
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG_TB_INTERCEPT_REDIRECTS = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False


if SQLALCHEMY_DATABASE_URI == "":
    print('DATABASE_URL is blank, please load and try again', flush=True)
    exit(1)
