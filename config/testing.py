# config/testing.py

from .default import *


# Parámetros para activar el modo debug
TESTING = True
DEBUG = True

APP_ENV = APP_ENV_TESTING
# este WTF_CSRF_... etc lo agregue yo. Fue lo único que agregue 28-5-22
WTF_CSRF_ENABLED = False 

SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_pass@host:port/db_name'