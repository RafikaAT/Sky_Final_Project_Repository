from flask import render_template
from application import app
from forms import SignUpForm
from forms import LoginForm

@app.route('/')
@app.route('/home', endpoint='home')
def home():
    return render_template('home.html', title="Home")

@app.route('/sign-up')
def sign_up():
    form = SignUpForm()
    return render_template('sign_up.html', title='Sign Up', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

@app.route('/film-reviews')
def film_reviews():
    return render_template('film_reviews.html', title="film-reviews")


@app.route('/new-gods-nezha-reborn')
def newgodsnezhareborn():
    return render_template('new-gods-nezha-reborn.html', title="New Gods: Nezha Reborn")

