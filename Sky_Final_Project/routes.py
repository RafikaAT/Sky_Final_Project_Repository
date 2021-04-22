from flask import render_template
from application import app


@app.route('/')
@app.route('/home', endpoint='home')
def home():
    return render_template('home.html', title="Home")

<<<<<<< HEAD
@app.route('/film-reviews')
def film_reviews():
    return render_template('film_reviews.html', title="film-reviews")
=======
@app.route('/new-gods-nezha-reborn')
def newgodsnezhareborn():
    return render_template('new-gods-nezha-reborn.html', title="New Gods: Nezha Reborn")

>>>>>>> 86f68bf59735bf03587a78ad1171ac2a943948f1
