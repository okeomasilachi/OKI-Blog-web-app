from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog.models import User
from flask_login import current_user

class Regfrom(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired(), Length(min=2, max=21)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_uname(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError(f"The user name {field.data} already Exist")

    def validate_email(self, field):
        email = User.query.filter_by(email=field.data).first()
        if email:
            raise ValidationError(f"{field.data} already in use by another user")


class Loginfrom(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),])
    remember = BooleanField('Remeber Me')
    submit = SubmitField('Login')
    


class UpdateAccountFrom(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired(), Length(min=2, max=21)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField("Update Profile Image", validators=[FileAllowed(["jpeg", "png", "jpg"])])
    submit = SubmitField('Update')

    def validate_username(self, field):
        if field.data != current_user.username:    
            user = User.query.filter_by(username=field.data).first()
            if user:
                raise ValidationError(f"The user name {field.data} already Exist")

    def validate_email(self, field):
        if field.data != current_user.email:
            email = User.query.filter_by(email=field.data).first()
            if email:
                raise ValidationError(f"{field.data} already in use by another user")

