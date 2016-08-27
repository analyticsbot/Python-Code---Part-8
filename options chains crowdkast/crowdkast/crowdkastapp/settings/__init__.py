from flask import Blueprint

settings = Blueprint('settings', __name__, template_folder="templates")
from views import *

