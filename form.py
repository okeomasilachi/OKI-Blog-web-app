from flask_wtf import Flask
from wtforms import stringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Lenght, Email, EqualTo


class Regfrom(Flaskfrom):
    uname = stringField('Username',
                        validators=[DataRequired(), Lenght(min=2, maxi=21)])
    email = stringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class Loginfrom(Flaskfrom):
    email = stringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),])
    remember = BooleanField('Remeber Me')
    submit = SubmitField('Login')

