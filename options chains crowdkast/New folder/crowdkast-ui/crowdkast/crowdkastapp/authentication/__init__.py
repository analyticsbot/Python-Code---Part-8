from flask import Blueprint
from flask.ext.login import LoginManager

## initialize login manager
login_manager = LoginManager()
authentication = Blueprint('authentication', __name__, template_folder="templates",static_folder='static',\
                           static_url_path='/static/authentication') #, url_prefix='/auth'
from views import *

@authentication.record_once
def on_load(state):
    login_manager.init_app(state.app)
    login_manager.login_view = '/authentication/signin'

@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)
