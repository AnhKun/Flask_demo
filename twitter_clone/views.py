from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import app, db, photos 
from models import User, Tweet
from forms import RegisterForm, LoginForm, TweetForm

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
    form = TweetForm()

    user_id = current_user.id
    tweets = Tweet.query.filter_by(user_id=user_id).order_by(Tweet.date_created.desc()).all()

    return render_template('timeline.html', form=form, tweets=tweets)

@app.route('/post_tweet', methods=["POST"])
@login_required
def post_tweet():
    form = TweetForm()
    if form.validate():
        tweet = Tweet(text=form.text.data, user_id=current_user.id, date_created=datetime.utcnow())
        db.session.add(tweet)
        db.session.commit()
        return redirect(url_for('timeline'))

    return flash('Error')

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        file_url = None
        if form.image.data:
            filename = photos.save(form.image.data)
            file_url = photos.path(filename)

        new_user = User(name=form.name.data, username=form.username.data, image=file_url, 
            password=generate_password_hash(form.password.data), join_date=datetime.utcnow())
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('profile'))
    return render_template('register.html', form=form)
