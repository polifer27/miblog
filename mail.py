
import os
from app import create_app, mail
from flask_mail import Message

#APP_SETTINGS_MODULE = config.dev

settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)
with app.app_context():
    msg = Message("Hola perinola", sender="fernandezpablo27@yahoo.com.ar", recipients=["pablofernandezdistribuidor@gmail.com"])

    msg.body = 'Bienvenid@ a mi bloghg probando'
    msg.html = '<p>Bienvenid@ a <strong>este bloghhhaaarsss</strong></p>'

    mail.send(msg)

