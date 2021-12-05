import os
from datetime import date
from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileField, FileAllowed
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(100))
    join_date = db.Column(db.DateTime)

class RegisterForm(FlaskForm):
    name = StringField("Full name", validators=[
        InputRequired("A full name is required"),
        Length(max=100, message="Your name cannot be more than 100 characters")
    ])
    username = StringField("Username", validators=[
        InputRequired("Username is required"),
        Length(max=30, message="Your username cannot be more than 30 characters")
    ])
    password = PasswordField("Password", validators=[
        InputRequired("Password is required"),
        Length(max=50, message="Your password cannot be more than 50 characters")
    ])
    image = FileField(validators=[
        FileAllowed(IMAGES, 'Only images are accepted.')
    ])
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
        InputRequired("Username is required"),
        Length(max=30, message="Your username cannot be more than 30 characters")
    ])
    password = PasswordField("Password", validators=[
        InputRequired("Password is required"),
        Length(max=50, message="Your password cannot be more than 50 characters")
    ])
    remember = BooleanField('Remember Me')
    submit = SubmitField()

def create_app():
    app = Flask(__name__)

    photos = UploadSet('photos', IMAGES)

    app.config['UPLOADED_PHOTOS_DEST'] = 'images'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///engage.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    db.init_app(app)
    migrate = Migrate(app, db)
    bootstrap = Bootstrap(app)
    configure_uploads(app, photos)

    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def index():
        form=LoginForm()
        return render_template('index.html', form=form)

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        if request.method=='GET':
            return redirect(url_for('index'))

        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user, remember=form.remember.data)
                    return redirect(url_for('profile'))
                flash('Login failed')
                
            else:
                flash('Login failed')

        return redirect(url_for('index'))

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/profile')
    @login_required
    def profile():
        return render_template('profile.html', current_user=current_user)

    @app.route('/timeline')
    def timeline():
        return render_template('timeline.html')

    @app.route('/register', methods=["GET", "POST"])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            file_url = None
            if form.image.data:
                filename = photos.save(form.image.data)
                file_url = photos.path(filename)

            new_user = User(name=form.name.data, username=form.username.data, image=file_url, 
                password=generate_password_hash(form.password.data), join_date=date.today())
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('profile'))
        return render_template('register.html', form=form)

    return app