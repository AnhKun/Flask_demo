from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import IMAGES

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

class TweetForm(FlaskForm):
    text = TextAreaField('Your tweet', validators=[
        InputRequired('Tweet is required!'),
        Length(max=140, message='Your tweet is over 140 characters!')
    ])