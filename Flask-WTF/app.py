from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, Form, FormField
from wtforms.validators import InputRequired, length, Email

class TelephoneForm(Form):
    country_code = IntegerField('country code')
    area_code = IntegerField('area code')
    number = StringField('number')

class LoginForm(FlaskForm):
    username = StringField('username', validators=[
        InputRequired('Input required!'),
        length(min=3, max=8, message='Your username id not the required length'),
    ])
    password = PasswordField('password', validators=[
        InputRequired(),
    ])
    age = IntegerField('age', default=24)
    yesno = BooleanField('yesno')
    email = StringField('email', validators=[
        Email(),
    ])

class NameForm(LoginForm):
    first_name = StringField('first name', validators=[InputRequired(),])
    last_name = StringField('last name', validators=[InputRequired(),])
    home_phone = FormField(TelephoneForm)
    mobile_phone = FormField(TelephoneForm)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Mysecret!'
    app.config['WTF_CSRF_ENABLED'] = True

    @app.route('/', methods=['GET', 'POST'])
    def index():
        form = NameForm()

        if form.validate_on_submit():

            return f'Country Code: {form.mobile_phone.country_code.data} Area Code: {form.home_phone.area_code.data} Number: {form.home_phone.number.data}'
            #return f'<h1>Username: {form.username.data} Password: {form.password.data} Age: {form.age.data}</h1>'

        return render_template('index.html', form=form)

    return app
