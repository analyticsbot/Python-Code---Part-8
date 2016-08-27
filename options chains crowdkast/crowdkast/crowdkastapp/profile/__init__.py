from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from flask import Blueprint

profile = Blueprint('profile', __name__, template_folder="templates",static_folder='static',\
                           static_url_path='/static/profile')
from views import *
