from flask import render_template, request
from flask import redirect, url_for, session
from crowdkastapp.authentication import Users

from flask.ext.classy import FlaskView, route
from flask.ext.login import login_required, current_user
from crowdkastapp.settings import settings
from crowdkastapp.authentication.views import hash_string
from crowdkastapp import db
import json, os

class SettingsView(FlaskView):
    @login_required
    def index(self):
	user = Users.query.filter_by(username=current_user.username).first()
        return render_template('settings.html', page_title='Customize your LinkedUp profile', user=user)

    @route('edit_username', methods=['POST'])
    @login_required
    def edit_username(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        if user == current_user:
            session['username'] = user.username = request.form["value"]            
            result = {}
            db.session.commit()
        return render_template('settings.html', page_title='Customize your LinkedUp profile', user=user)

	
    # edit full name
    @route('edit_email', methods=['POST'])
    @login_required
    def edit_email(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        if user == current_user:
            user.email = request.form["value"]
            result = {}
            db.session.commit()
            return json.dumps(result)  #or, as it is an empty json, you can simply use return "{}"

	
	# edit location
    @route('edit_password', methods=['POST'])
    @login_required
    def edit_password(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        if user == current_user:
            user.password = hash_string(request.form["value"])
            result = {}
            db.session.commit()
            return json.dumps(result)

SettingsView.register(settings)
