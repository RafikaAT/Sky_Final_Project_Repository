import app as app
from flask import Flask, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from application import app

username = 'newuser'
password = 'password'
userpass = 'mysql+pymysql://' + username + ':' + password + '@'
server = '127.0.0.1'
dbname = '/db'

app = Flask(__name__)
app.secret_key = 'skyGIT'
# put them all together as a string that shows SQLAlchemy where the database is
app.config['SQLALCHEMY_DATABASE_URI'] = userpass + server + dbname
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://newuser:password@localhost/db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'orange-color'


from application import routes