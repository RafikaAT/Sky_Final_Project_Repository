from datetime import datetime
from flask import render_template, flash, render_template, url_for, redirect, Flask
from flask_sqlalchemy import SQLAlchemy
from application import app
from forms import SignUpForm
from forms import LoginForm, PostComment



@app.route('/')
@app.route('/home', endpoint='home')
def home():
    return render_template('home.html', title="Home")


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('sign_up.html', title='Sign Up', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/film-reviews')
def film_reviews():
    return render_template('film_reviews.html', title="film-reviews")


@app.route('/new-gods-nezha-reborn')
def newgodsnezhareborn():
    return render_template('new-gods-nezha-reborn.html', title="New Gods: Nezha Reborn")

@app.route('/comments/new',methods=['GET', 'POST'])
# @login_required
def new_comment():
    form = PostComment()
    if form.validate_on_submit():
        flask("Your comment has been created", "success")
        return redirect(url_for('home'))
    return render_template('new_comment.html', title="New Comment", form=form)
