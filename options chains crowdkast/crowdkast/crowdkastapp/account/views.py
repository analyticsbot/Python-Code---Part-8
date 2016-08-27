import json, os 
from flask.ext.classy import FlaskView, route
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename

from crowdkastapp.account import account
from crowdkastapp.profile import profile
from flask import render_template, request
from crowdkastapp.authentication import Users
from crowdkastapp import db
from crowdkastapp.config import *
from crowdkastapp import application
from crowdkastapp.profile.models import * 

## editing the account details. check if the user is logged in and is editing self details.

class AccountView(FlaskView):
    # edit position
    @route('edit_position', methods=['POST'])
    @login_required
    def edit_position(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        if user == current_user:
            user.position = request.form["value"]
            result = {}
            db.session.commit()
            return json.dumps(result)
	
    # edit full name
    @route('edit_fullname', methods=['POST'])
    @login_required
    def edit_fullname(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        if user == current_user:
            user.fullname = request.form["value"]
            result = {}
            db.session.commit()
            return json.dumps(result)  #or, as it is an empty json, you can simply use return "{}"

	
	# edit location
    @route('edit_location', methods=['POST'])
    @login_required
    def edit_location(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        if user == current_user:
            user.location = request.form["value"]
            result = {}
            db.session.commit()
            return json.dumps(result)
	
	# edit Linkedin URL
    @route('editLinkedin', methods=['POST'])
    @login_required
    def editLinkedin(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        if user == current_user:
            user.linkedin = request.form["value"] if request.form["value"].startswith('http://')==True \
                            else request.form["value"] if request.form["value"].startswith('https://')==True \
                            else 'http://' + request.form["value"]
            result = {}
            db.session.commit()
            return json.dumps(result)
	
    @route('editStackOverflow', methods=['POST'])
    @login_required
    def editStackOverflow(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        if user == current_user:
            user.stackoverflow = request.form["value"] if request.form["value"].startswith('http://')==True \
                            else request.form["value"] if request.form["value"].startswith('https://')==True \
                            else 'http://' + request.form["value"]
            result = {}
            db.session.commit()
            return json.dumps(result)
	
    # edit about me URL
    @route('editAboutMe', methods=['POST'])
    @login_required
    def editAboutMe(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        if user == current_user:
            user.aboutme = request.form["value"] if request.form["value"].startswith('http://')==True \
                            else request.form["value"] if request.form["value"].startswith('https://')==True \
                            else 'http://' + request.form["value"]
            result = {}
            db.session.commit()
            return json.dumps(result)
	
    # edit visual CV URL
    @route('editVisualCV', methods=['POST'])
    @login_required
    def editVisualCV(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        if user == current_user:
            user.visualcv = request.form["value"] if request.form["value"].startswith('http://')==True \
                            else request.form["value"] if request.form["value"].startswith('https://')==True \
                            else 'http://' + request.form["value"]
            result = {}
            db.session.commit()
            return json.dumps(result)
	
    # edit facebook URL
    @route('editFacebook', methods=['POST'])
    @login_required
    def editFacebook(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        if user == current_user:
            user.facebook = request.form["value"] if request.form["value"].startswith('http://')==True \
                            else request.form["value"] if request.form["value"].startswith('https://')==True \
                            else 'http://' + request.form["value"]
            result = {}
            db.session.commit()
            return json.dumps(result)
	
    # edit Twitter URL
    @route('editTwitter', methods=['POST'])
    @login_required
    def editTwitter(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        if user == current_user:
            user.twitter = request.form["value"] if request.form["value"].startswith('http://')==True \
                            else request.form["value"] if request.form["value"].startswith('https://')==True \
                            else 'http://' + request.form["value"]
            result = {}
            db.session.commit()
            return json.dumps(result)
	
    # edit Quora URL
    @route('editQuora', methods=['POST'])
    @login_required
    def editQuora(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        if user == current_user:
            user.quora = request.form["value"] if request.form["value"].startswith('http://')==True \
                            else request.form["value"] if request.form["value"].startswith('https://')==True \
                            else 'http://' + request.form["value"]
            result = {}
            db.session.commit()
            return json.dumps(result)
    
    # edit Github URL
    @route('editGithub', methods=['POST'])
    @login_required
    def editGithub(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        if user == current_user:
            user.github = request.form["value"] if request.form["value"].startswith('http://')==True \
                            else request.form["value"] if request.form["value"].startswith('https://')==True \
                            else 'http://' + request.form["value"]
            result = {}
            db.session.commit()
            return json.dumps(result)
	
    # edit Github URL
    @route('addEducation', methods=['POST'])
    @login_required
    def addEducation(self):
        id = request.form["pk"]
        user = Users.query.get(id)
        if user == current_user:
	    print request.form["value"]
            result = {}
            #univ = user.universities()
            user.universities.append(Universities(university = request.form["value"]))
            
            #db.session.add(Universities(university = request.form["value"]))
            db.session.commit()
            return json.dumps(result)

    # edit Github URL
    @route('editEducation', methods=['POST'])
    @login_required
    def editEducation(self):
        id = request.form["pk"]
        univ_id = request.form["name"]
        print univ_id
        user = Users.query.get(id)        
        if user == current_user:
	    print request.form["value"]
            result = {}
            #univ = user.universities()
            univ = Universities.query.get(univ_id)
            univ.university = request.form["value"]
            #db.session.add(Universities(university = request.form["value"]))
            db.session.commit()
            return json.dumps(result)

    @route('deleteUniversity', methods = ['GET', 'POST'])
    @login_required
    def deleteUniversity(self):
        univ_id = request.args.get('univ')
        id = request.args.get('id')
        user = Users.query.get(id)
        if user == current_user: 
            univ = Universities.query.get(univ_id)
            Universities.query.filter_by(id=univ_id).delete()
            db.session.commit()
            print id, univ_id, univ
            result = {}
            return json.dumps(result)

    # upload avatar
    @route('upload_avatar', methods=['POST'])
    @login_required
    def upload_avatar(self):
        if request.method == 'POST':
            id = request.form["avatar_user_id"]
            file = request.files['file']
            if file and allowed_file(str.lower(str(file.filename))):
                user = Users.query.get(id)
                filename = user.username + "_" + secure_filename(file.filename)
		if os.environ['CONFIG_VARIABLE'] == "config.DevelopmentConfig":                    
                    file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
                else:                    
                    file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
                img = "/static/upload/" + filename
                

                user.avatar = img
                db.session.commit()
                return img

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in application.config['ALLOWED_EXTENSIONS']

## register the blueprint
AccountView.register(account)
