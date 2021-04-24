from flask import Flask
from forms import SignUpForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e3c56yt2bof7'
from application import routes

