import os
from flask import Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail, Message

## import the configuration settings specific to the working environment
from config import *

application = Flask(__name__, static_folder= os.path.join(os.path.dirname(__file__), "..", "static"))

if os.environ['CONFIG_VARIABLE'] == "config.DevelopmentConfig":
        application.config.from_object(config.DevelopmentConfig)
elif os.environ['CONFIG_VARIABLE'] == "config.ProductionConfig":
        application.config.from_object(config.ProductionConfig)

db = SQLAlchemy(application)
mail = Mail(application)

## initialize the blueprint
mypage = Blueprint('mypage', __name__)

## import all the views, blueprints
from views import *

from authentication import authentication


## register all the blueprints
application.register_blueprint(mypage)
application.register_blueprint(authentication)
