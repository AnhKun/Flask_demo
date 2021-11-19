from flask import Flask
from flask_mail import Mail, Message
import smtplib

def create_app():
    app = Flask(__name__)

    app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = '****@yahoo.com'
    app.config['MAIL_PASSWORD'] = '****'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_DEFAULT_SENDER'] = '****@yahoo.com'

    mail = Mail()
    mail.init_app(app)

    @app.route('/')
    def index():
        msg = Message('Hello From Flask', recipients=['****@gmail.com'])

        s = smtplib.SMTP_SSL('smtp.mail.yahoo.com')
        s.login('****@yahoo.com', '****')

        mail.send(msg)

        return '<h1>Sent</h1>'

    return app