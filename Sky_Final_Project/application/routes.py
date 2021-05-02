from flask import flash, render_template, url_for, redirect, request
from application import app, db, bcrypt
from forms import SignUpForm
from forms import LoginForm, PostComment
from models import User, Post
from application import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home', endpoint='home')
def home():
    return render_template('home.html', title="Home")


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    username = form.username.data
    email = form.email.data
    password = form.password.data

    if request.method == 'POST' and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('sign_up.html', title='Sign Up', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    # posts = Post.query.filter_by(author=form.current_user.data)
    # posts = Post.query.filter_by(user_id=current_user.id).all()
    posts = Post.query.filter_by(user_id=current_user.id)
    return render_template('account.html', title='Your Posts', posts=posts)

@app.route('/film-reviews')
def film_reviews():
    posts = Post.query.all()
    return render_template('film_reviews.html', title="film-reviews", posts=posts)


@app.route('/new-gods-nezha-reborn')
def newgodsnezhareborn():
    posts = Post.query.current_user()  #HERE
    return render_template('new-gods-nezha-reborn.html', title="New Gods: Nezha Reborn", posts=posts)


@app.route('/comments/new', methods=['GET', 'POST'])
@login_required
def new_comment():
    form = PostComment()
    if request.method == 'POST' and form.validate_on_submit():
        comment = Post(title=form.title.data, snippet=form.snippet.data, content=form.content.data, author=current_user)
        if current_user.is_authenticated:
            db.session.add(comment)
            db.session.commit()
            flash("Your comment has been sent to the authors for review", "success")
            return redirect(url_for('home')) #This will have to be changed into whichever page's comment we're on.
    return render_template('new_comment.html', title="New Comment", form=form)


@app.route('/comments/<int:comment_id>')
def blogreview(comment_id):
    post = Post.query.get_or_404(comment_id)
    # image_file_review = url_for('/static/', filename=f'review_images/{post.image_file_review}')
    # image_file_review=(url_for('static', filename='review_images/' + comment_id.image_file_review)) #ALSO add IMAGE FILE REVIEW BELOW
    return render_template('blogpost.html', title=post.title, review=post.content, post=post)