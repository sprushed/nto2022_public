from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=64)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=64)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=64)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=64)])

