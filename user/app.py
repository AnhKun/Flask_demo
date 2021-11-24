from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, UserMixin, SQLAlchemyAdapter, login_required, current_user
from flask_mail import Mail

app = Flask(__name__)

app.config['SECRET_KEY'] = '****'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['CSRF_ENABLED'] = True
app.config['USER_ENABLE_EMAIL'] = True
app.config['USER_AFTER_REGISTER_ENDPOINT'] = 'user.login'
#app.config.from_pyfile('config.cfg')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USERNAME'] = 'n****@gmail.com'
app.config['MAIL_PASSWORD'] = '****'  # generate app password
app.config['MAIL_DEFAULT_SENDER'] = 'n****@gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False

db = SQLAlchemy(app)
mail = Mail(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)

@app.route('/')
def index():
    return '<h1>This is the unprotected homepage!</h1>'

@app.route('/profile')
@login_required
def profile():
    return '<h1>Hello, {}</h1>'.format(current_user.username)


if __name__ == '__main__':
    app.run(debug=True)