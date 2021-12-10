import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trendy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
configure_uploads(app, photos)

from views import *

if __name__ == '__main__':
    app.run(debug=True)