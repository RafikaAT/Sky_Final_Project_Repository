from flask import Flask, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'e3c56yt2bof7'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:password@localhost/movieblog"

db = SQLAlchemy(app)

from application import routes
