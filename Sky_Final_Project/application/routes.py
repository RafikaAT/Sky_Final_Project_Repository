from flask import flash, render_template, url_for, redirect, request
from application import app
from forms import SignUpForm
from forms import LoginForm, PostComment
from models import User
from application import db


@app.route('/')
@app.route('/home', endpoint='home')
def home():
    return render_template('home.html', title="Home")


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    username = form.username.data
    email = form.email.data

    if request.method == 'POST' and form.validate_on_submit():
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()

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
        flash("Your comment has been sent to the authors for review", "success")
        return redirect(url_for('home'))
    return render_template('new_comment.html', title="New Comment", form=form)

