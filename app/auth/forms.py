from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo, Regexp
from flask_babel import _, lazy_gettext as _l

from app.models import User


class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Keep me logged in'))
    submit = SubmitField(_l('Log In'))


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[
        DataRequired(),
        Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Username must have only letters, numbers, dots or underscores')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(_('Email already registered.'))

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(_('Username already in use.'))

