from flask import render_template, request, flash, request, redirect, url_for, session, flash, g, \
     render_template

from flask.ext.classy import FlaskView, route
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from forms import *
from models import *
from crowdkastapp.authentication import authentication
from crowdkastapp import application
import md5, os
from flask_oauth import OAuth
from flask_oauthlib.client import OAuth
from generate_token import generate_confirmation_token, confirm_token
import datetime
from crowdkastapp.email import send_email

oauth = OAuth(application)

twitter = oauth.remote_app(
    'twitter',
    consumer_key=application.config['CONSUMER_KEY'],
    consumer_secret=application.config['CONSUMER_SECRET'],
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
)

@twitter.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']

@application.before_request
def before_request():
    g.user = None
    if 'twitter_oauth' in session:
        g.user = session['twitter_oauth']

facebook = oauth.remote_app(
    'facebook',
    consumer_key=application.config['FACEBOOK_APP_ID'],
    consumer_secret=application.config['FACEBOOK_APP_SECRET'],
    request_token_params={'scope': 'email'},
    base_url='https://graph.facebook.com',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    access_token_method='GET',
    authorize_url='https://www.facebook.com/dialog/oauth'
)

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

## method to hash the password before storing in db. Never ever store passwords as it is. 
def hash_string(string):
    password_hash = string
    return password_hash
    #return md5.new(password_hash).hexdigest()

class AuthenticationView(FlaskView):
    @route('signin', methods=['GET', 'POST'])
    def signin(self):
        if request.method == 'POST':
            if os.environ['CONFIG_VARIABLE'] == "config.DevelopmentConfig":
                if current_user is not None and current_user.is_authenticated:            	
                    return redirect(url_for('mypage.index'))
            if os.environ['CONFIG_VARIABLE'] == "config.ProductionConfig":
                if current_user is not None and current_user.is_authenticated():            	
                    return redirect(url_for('mypage.index'))

            form = SigninForm(request.form)
            if form.validate():                
                user = Users.query.filter_by(username=form.username.data).first()
                
                if user is None:
		    # username not found in db
                    form.username.errors.append('Username not found')
                    return render_template('signin.html', signin_form = form, page_title='Sign In | Crowdkast',signinpage_form = SigninForm())
                if user.password != hash_string(form.password.data):
		    # username found but password not the same as in db
                    form.password.errors.append('Passwords did not match. Try again!')
                    return render_template('signin.html', signin_form = form, page_title='Sign In | Crowdkast', signinpage_form = SigninForm())

                ## add the check to see if the user is confirmed or not
                ## else return to the flash a message saying
                ## confirm the email
                if not user.confirmed:
                    flash("Please click on the confirmation link sent to your email")
                    return render_template('signin.html', signin_form = form, page_title='Sign In | Crowdkast', signinpage_form = SigninForm())
				
		## if the user is found and password is correct, login
                login_user(user, remember=form.remember_me.data)
		# store the following values in the session dictionary
                session['signed'] = True
                session['username'] = user.username
				
		## if the user was looking for page which needs login, proceed to the page after login
                if session.get('next'):
                    next_page = session.get('next')
                    session.pop('next')
                    return redirect(next_page)
                else:                    
                    return redirect(url_for('mypage.index', username =user.username))
            return render_template('signin.html', signin_form=form, page_title='Sign In | Linkedup', signinpage_form = SigninForm())
        else:
            session['next'] = request.args.get('next')
            return render_template('signin.html', signin_form=SigninForm(), signinpage_form = SigninForm(), page_title='Sign In | Linkedup')
    
    
    @route('twitterlogin', methods=['GET', 'POST'])
    def twitterlogin(self):
        """Calling into authorize will cause the OpenID auth machinery to kick
        in.  When all worked out as expected, the remote application will
        redirect back to the callback URL provided.
        """
        return twitter.authorize(callback=url_for('authentication.AuthenticationView:oauthorized',
            next=request.args.get('next') or request.referrer or None))

    @route('oauthorized', methods=['GET', 'POST'])
    def oauthorized(self):
        resp = twitter.authorized_response()
        username = resp['screen_name']
        if resp is None:
            flash('You denied the request to sign in.')
        else:
            session['twitter_oauth'] = resp
            session['login_method'] = 'twitter'
            
        login_user(username)
        return redirect(url_for('mypage.index', username = username))

##    @route('twitterlogout', methods=['GET', 'POST'])
##    def logout():
##        session.pop('user_id', None)
##        flash('You were signed out')
##        return redirect(request.referrer or url_for('mypage.index'))

    @route('logout')
    @login_required
    def logout(self):
        session.clear()
        logout_user()
        return redirect(url_for('mypage.index'))

    @route('facebooklogin', methods=['GET', 'POST'])
    def facebooklogin(self):
        callback = url_for(
            'authentication.AuthenticationView:facebook_authorized',
            next=request.args.get('next') or request.referrer or None,
            _external=True
        )
        return facebook.authorize(callback='http://localhost:8000/')

    @route('authorized')
    def facebook_authorized(self):
        resp = facebook.authorized_response()
        if resp is None:
            return 'Access denied: reason=%s error=%s' % (
                request.args['error_reason'],
                request.args['error_description']
            )
        if isinstance(resp, OAuthException):
            return 'Access denied: %s' % resp.message

        session['oauth_token'] = (resp['access_token'], '')
        me = facebook.get('/me')
        return 'Logged in as id=%s name=%s redirect=%s' % \
            (me.data['id'], me.data['name'], request.args.get('next'))

    @route('resend', methods = ['POST'])
    def resend_confirmation(self):
        if request.method == 'POST':
            token = generate_confirmation_token(request.form['email'])
            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(current_user.email, subject, html)
            flash('A new confirmation email has been sent.', 'success')
            return redirect(url_for('user.unconfirmed'))

    @route('confirm/<token>')
    def confirm_email(self, token=None):
        try:
            email = confirm_token(token)
        except:
            flash('The confirmation link is invalid or has expired.', 'danger')
        user = User.query.filter_by(email=email).first_or_404()
        if user.confirmed:
            flash('Account already confirmed. Please login.', 'success')
        else:
            user.confirmed = True
            user.confirmed_on = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
            flash('You have confirmed your account. Thanks!', 'success')
        return redirect(url_for('mypage.index'))

    @route('reset-password', methods=('GET', 'POST',))
    def forgot_password(self):
        if request.method == 'GET':
            token = request.args.get('token',None)
            if token and verified_result:
                is_verified_token = True
                password_submit_form = ResetPasswordSubmit(request.form)
                if password_submit_form.validate_on_submit():
                    verified_result.password = generate_password_hash(password_submit_form.password.data)
                    verified_result.is_active = True
                    db.session.add(verified_result)
                    db.session.commit()
                    #return "password updated successfully"
                    flash("password updated successfully")
                    return redirect(url_for('authentication.AuthenticationView:signin'))
        
        form = ResetPasswordRequestForm(request.form) #form
        if form.validate_on_submit():
            email = form.email.data
            print email
            user = User.query.filter_by(email=email).first()
            if user:
                token = generate_confirmation_token(email)
                confirm_url = url_for('confirm_email', token=token, _external=True)
                html = render_template('activate.html', confirm_url=confirm_url)
                subject = "Please confirm your email at Crowdkast!"
                send_email(current_user.email, subject, html)
                flash('A confirmation email has been sent. Please click on the activation link', 'success')
        return render_template('forget_password.html', form=form)

    
    @route('signup', methods=['GET', 'POST'])
    def signup(self):
        if request.method == 'POST':
            form = SignupForm(request.form)
            if form.validate():
                # initialize the User class from authentication
                user = Users()
                form.populate_obj(user)
				
		# check if the user or email entered already exists in the db
                user_exist = Users.query.filter_by(username=form.username.data).first()
                email_exist = Users.query.filter_by(email=form.email.data).first()

                if user_exist:
                    form.username.errors.append('Username already taken')

                if email_exist:
                    form.email.errors.append('Email already in use')

                if user_exist or email_exist:
                    return render_template('signup.html',
                                           signin_form=SigninForm(),
                                           form = form,
                                           page_title='Signup | Crowdkast')

                else:
                    user.fname = user.fname
                    user.username = user.username
                    user.lname = user.lname
                    user.password = hash_string(user.password)
                    user.email = user.email
                    user.avatar = ''
                    user.active = True
                    user.confirmed = False

                    db.session.add(user)
                    db.session.commit()

                    token = generate_confirmation_token(user.email)
                    confirm_url = url_for('user.confirm_email', token=token, _external=True)
                    html = render_template('user/activate.html', confirm_url=confirm_url)
                    subject = "Please confirm your email"
                    send_email(user.email, subject, html)
                    
                    return render_template('signup-success.html',
                                           user=user,
                                           signin_form=SigninForm(),
                                           page_title='Sign Up Successfull!')

            else:
                return render_template('signup.html',
                                       form=form,
                                       signin_form=SigninForm(),
                                       page_title='Signup | Linkedup')
        return render_template('signup.html',
                               form=SignupForm(),
                               signin_form=SigninForm(),
                               title='Signup | Crowdkast')

AuthenticationView.register(authentication)
