import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileField, FileAllowed
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, IMAGES

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(30))
    password = db.Column(db.String(50))
    image = db.Column(db.String(100))

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

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/profile')
    def profile():
        return render_template('profile.html')

    @app.route('/timeline')
    def timeline():
        return render_template('timeline.html')

    @app.route('/register', methods=["GET", "POST"])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            filename = photos.save(form.image.data)
            image_url = photos.url(filename)
            return '<h1>{}</h1>'.format(image_url)
        return render_template('register.html', form=form)

    return app