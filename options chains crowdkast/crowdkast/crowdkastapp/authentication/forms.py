from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, validators, HiddenField, TextAreaField, BooleanField
from wtforms.validators import Required, EqualTo, Optional, Length, Email

## sign up form
class SignupForm(Form):
        username = TextField('Username', validators=[Required('Required Field'), Length(min=1, message=(u'Username too short'))])
        fname = TextField('First name', validators=[Required('Required Field')])
        lname = TextField('Last name', validators=[Required('Required Field')])
        email = TextField('Email address', validators=[
            Required('Please provide a valid email address!'),
            Length(min=2, message=(u'Email address too short')),
            Email(message=(u'That\'s not a valid email address'))
            ])
        password = PasswordField('Pick a secure password', validators=[
            Required('Required Field'),
            Length(min=0, message=(u'Please give a longer password.')),
			EqualTo('confirm', message='Passwords must match')
            ])
        confirm = PasswordField('Please repeat your password')
        recaptcha = RecaptchaField()
        agree = BooleanField('By clicking Join now, you agree to <a href="#">Crowkast\'s User Agreement</a>', validators=[Required(u'You must accept our Terms of Service')])
        

## sign in form
class SigninForm(Form):
        username = TextField('Username', validators=[
            Required(),
            validators.Length(min=0, message=(u'Username too short'))
            ])
        password = PasswordField('Password', validators=[
            Required(),
            validators.Length(min=0, message=(u'Longer password required'))
            ])
        remember_me = BooleanField('Remember me', default = True)

## sign in form
class ContactForm(Form):
        name = TextField('Name', validators=[
            Required(),
            validators.Length(min=1, message=(u'Name too short'))
            ])
        email = TextField('Email address', validators=[
            Required('Please provide a valid email address!'),
            Length(min=2, message=(u'Email address too short')),
            Email(message=(u'That\'s not a valid email address'))
            ])
        phone = TextField('Phone', validators=[
            Required(),
            validators.Length(min=0, message=(u''))
            ])
        company = TextField('Company', validators=[
            Required(),
            validators.Length(min=0, message=(u''))
            ])
        

class ResetPasswordSubmit(Form):
    password = PasswordField('Password', validators=[Required('Required Field')] )
    confirm = PasswordField('Confirm Password')

class ResetPasswordRequestForm(Form):
    email = TextField('Email Address')
