from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    first_name = StringField(
        'First Name', validators=[DataRequired(), Length(min=2, max=50)]
    )
    last_name = StringField(
        'Last Name', validators=[DataRequired(), Length(min=2, max=50)]
    )
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6)]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Create Account')
