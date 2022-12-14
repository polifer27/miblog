import logging
from flask_mail import Mail # 1. Importo un objeto Mail
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler, SMTPHandler
from app.common.filters import format_datetime
#from flask_bootstrap import Bootstrap5

#bootstrap = Bootstrap5
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail() # 2. Instancio un objeto de tipo Mail

# app/__init__.py

# app/__init__.py

def create_app(settings_module='config.development'):
    app = Flask(__name__, instance_relative_config=True)
    # Load the config file specified by the APP environment variable
    #db.init_app(app)

    
    
   # with app.app_context():
        

    app.config.from_object(settings_module)
    # Load the configuration from the instance folder
    if app.config.get('TESTING', False):
        app.config.from_pyfile('config-testing.py', silent=True)
    else:
        app.config.from_pyfile('config.py', silent=True)

    configure_logging(app)

    #login_manager.init_app(app)
    #login_manager.login_view = "auth.login"

        

    app.config[
            "SECRET_KEY"
        ] = "7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe"
    app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "postgresql+psycopg2://postgres:1234@localhost:5432/miniblog"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#postgresql+psycopg2://postgres:1234@localhost:5432/miniblog
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    db.init_app(app)
    migrate.init_app(app, db) # Se inicializa el objeto migrate
    mail.init_app(app) # Inicializo el objeto mail
    
    # Registro de los filtros
    register_filters(app)

    # Registro de los Blueprints
    from .auth import auth_bp

    app.register_blueprint(auth_bp)

    from .admin import admin_bp

    app.register_blueprint(admin_bp)
            
    from .public import public_bp
    app.register_blueprint(public_bp)
    # Custom error handlers
    register_error_handlers(app)

    return app

def register_filters(app):
    app.jinja_env.filters['datetime'] = format_datetime    

def register_error_handlers(app):

    @app.errorhandler(401)
    def error_404_handler(e):
        return render_template('401.html'), 401    

    @app.errorhandler(404)
    def error_404_handler(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def base_error_handler(e):
        return render_template('500.html'), 500    

def verbose_formatter():
    return logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S'
    )

def configure_logging(app):

    # Elimina los manejadores por defecto de la app
    del app.logger.handlers[:]
    
    LOG_LEVEL = logging.DEBUG
    LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
    from colorlog import ColoredFormatter
    logging.root.setLevel(LOG_LEVEL)
    formatter = ColoredFormatter(LOGFORMAT)
    #setlevel

    loggers = [app.logger, logging.getLogger('sqlalchemy')]
    handlers = []

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(verbose_formatter())
    
    if (app.config['APP_ENV'] == app.config['APP_ENV_LOCAL']) or (
            app.config['APP_ENV'] == app.config['APP_ENV_TESTING']) or (
            app.config['APP_ENV'] == app.config['APP_ENV_DEVELOPMENT']):
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        handlers.append(console_handler)
    elif app.config['APP_ENV'] == app.config['APP_ENV_PRODUCTION']:
        console_handler.setLevel(logging.INFO)
        handlers.append(console_handler)
        console_handler.setFormatter(formatter)

        mail_handler = SMTPHandler((app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                                   app.config['DONT_REPLY_FROM_EMAIL'],
                                   app.config['MAIL_USERNAME'],
                                   '[Error][{}] La aplicaci??n fall??'.format(app.config['APP_ENV']),
                                   (app.config['ADMINS'],
                                    app.config['MAIL_PASSWORD']),
                                   ())
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(mail_handler_formatter())
        handlers.append(mail_handler)

    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)


def mail_handler_formatter():
    return logging.Formatter(
        '''
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s.%(msecs)d

            Message:

            %(message)s
        ''',
        datefmt='%d/%m/%Y %H:%M:%S'
    )      
    
    