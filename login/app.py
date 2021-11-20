from flask import Flask, request, render_template, session, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user, \
    fresh_login_required
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse, urljoin

login_manager = LoginManager()
db = SQLAlchemy()

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))

    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    login_manager.init_app(app)
    db.init_app(app)

    login_manager.login_view = 'login'
    login_manager.login_message = 'You cannot access that page. You need to login first.'
    login_manager.refresh_view = 'login'
    login_manager.needs_refresh_message = 'You need to login again!'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/profile')
    @login_required
    def profile():
        return '<h1>You are in the profile, {}.</h1>'.format(current_user.name)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('name')
            remember_me = request.form.get('remember_me')
            user = User.query.filter_by(name=username).first()
            if not user:
                return '<h1>User does not exist!</h1>'

            login_user(user, remember=remember_me)

            if 'next' in session and session['next']:
                if is_safe_url(session['next']):
                    return redirect(session['next'])

            return redirect(url_for('index'))

        session['next'] = request.args.get('next')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return '<h1>You are now log out!</h1>'

    @app.route('/')
    def index():
        return '<h1>You are now on the homepage</h1>'

    @app.route('/change')
    @fresh_login_required
    def change():
        return '<h1>This is for fresh login only!</h1>'

    return app