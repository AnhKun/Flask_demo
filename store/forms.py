from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField, SelectField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import IMAGES


class AddProduct(FlaskForm):
    name = StringField('Product Name', validators=[
        InputRequired('Name is required!')
    ])
    price = IntegerField('Product Price', validators=[
        InputRequired('Price is required!')
    ])
    stock = IntegerField('Openning Stock')
    description = TextAreaField('Description')
    image = FileField('Product Image', validators=[
        FileAllowed(IMAGES, 'Only images are accepted!'),
        InputRequired()
    ])

class AddToCart(FlaskForm):
    quantity = IntegerField('Quantity', validators=[InputRequired()])
    product_id = HiddenField('ID')

class Checkout(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    phone_number = StringField('Phone Number')
    email = StringField('Email')
    address = StringField('Address')
    city = StringField('City')
    state = SelectField('State', choices=[
        ('CA', 'California'), 
        ('WA', 'Washington'), 
        ('NV', 'Nevada')
    ])
    country = SelectField('Country', choices=[
        ('US', 'United State'), 
        ('UK', 'United Kingdom'), 
        ('FRA', 'France')
    ])
    payment_type = SelectField('Payment Type', choices=[
        ('CK', 'Check'),
        ('WT', 'Wire Transfer')
    ])