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
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', title="Home", posts=posts)


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
            flash('Login unsuccessful. Please check email and password.', 'danger')
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
    page = request.args.get('page', 1, type=int)
    # posts = Post.query.paginate(page=page, per_page=5) This is older version, pre-arranging by date
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
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
        comment = Post(title=form.title.data, content=form.content.data, author=current_user)
        if current_user.is_authenticated:
            db.session.add(comment)
            db.session.commit()
            flash("Your review has been posted!", "success")
            return redirect(url_for('home')) #This will have to be changed into whichever page's comment we're on.
    return render_template('new_comment.html', title="New Review", form=form, legend='New Review')


@app.route('/comments/<int:comment_id>')
def blogreview(comment_id):
    post = Post.query.get_or_404(comment_id)
    # image_file_review = url_for('/static/', filename=f'review_images/{post.image_file_review}')
    # image_file_review=(url_for('static', filename=# image_file_review = url_for('/static/', filename=f'review_images/{post.image_file_review}')
    #     # image_file_review=(url_for('static', filename='review_images/' + comment_id.image_file_review)'review_images/' + comment_id.image_file_review)) #ALSO add IMAGE FILE REVIEW BELOW
    return render_template('blogpost.html', title=post.title, review=post.content, post=post)


@app.route('/film-reviews/<int:comment_id>')
def post(comment_id):
    post = Post.query.get_or_404(comment_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/film-reviews/update/<int:comment_id>", methods=['GET', 'POST'])
@login_required
def update_post(comment_id):
    post = Post.query.get_or_404(comment_id)
    form = PostComment()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your review has been updated!', 'success')
        return redirect(url_for('blogreview', comment_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('new_comment.html', title='Edit Review', form=form, legend='Edit Review')


@app.route("/film-reviews/delete/<int:comment_id>", methods=['POST'])
@login_required
def delete_post(comment_id):
    post = Post.query.get_or_404(comment_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'danger')
    return redirect(url_for('home'))


@app.route('/user/<string:username>')
def username_post(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)