from flask import render_template, flash
from crowdkastapp import mypage

from authentication.forms import * #users can signin/signup from within our main page
from authentication.models import * #.. therefore we need the auth models


from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required

## add the login required handler
@login_required
@mypage.route('/')
@mypage.route('/<username>')
def index(username=None):
##    if username is None:
##        return render_template('homepage.html', page_title='LinkedUp - Login or Signup', signin_form=SigninForm())
##
##    user = Users.query.filter_by(username=username).first()
##    if user is None:
##	# return to the sign up page with a message, the user does not exist
##        return render_template('signup.html', page_title='Profile Not Found | LinkedUp', message = 'An exact match could not be found. Sign in or join LinkedUp.', signin_form=SigninForm(), form = SignupForm())
##    else:
##        return render_template('crowdkast/index.html', page_title= user.fname + " | LinkedUp", \
##                               user=user, contactForm = ContactForm())
    return render_template('crowdkast/index.html')
