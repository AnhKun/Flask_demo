from flask import Flask, render_template, request
from flask_babel import Babel, get_locale, format_date, format_datetime
from datetime import date, datetime

app = Flask(__name__)
babel = Babel(app)

@babel.localeselector
def localeselector():
    #return 'en_US'
    return request.accept_languages.best_match(['en_US', 'en_GB', 'es_ES', 'vi_VN'])

@app.route('/')
def index():
    d = date.today()
    dt = datetime.today()

    local_date = format_date(d)
    local_datetime = format_datetime(dt)

    return render_template('index.html', locale=get_locale(), local_date=local_date, \
                           local_datetime=local_datetime)

if __name__ == '__main__':
    app.run(debug=True)