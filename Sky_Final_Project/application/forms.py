from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User
from flask_login import current_user


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6, max=20), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f'{username.data} username is taken. Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f'{email.data} email is taken. Please choose a different one')


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PostComment(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField("Submit")


    # def user_logged_out(self):
    #     if not current_user.is_authenticated:
    #         raise ValidationError("You must be logged in to leave a comment.")
