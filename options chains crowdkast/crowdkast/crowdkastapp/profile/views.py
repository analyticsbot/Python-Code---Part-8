import json
from flask.ext.classy import FlaskView, route
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from crowdkastapp.profile import profile
from models import *
from forms import *
from flask import render_template, request
from crowdkastapp.authentication.models import Users
from flask import redirect, url_for, session
from werkzeug.datastructures import ImmutableMultiDict

class ProfileView(FlaskView):
    @route('add_update', methods=['POST'])
    @login_required
    def add_update(self):
        form = SkillForm(request.form)
	
        if form.validate():
            result = {}
            result['iserror'] = False

            if not form.skill_id.data:
                user = Users.query.filter_by(username=session['username']).first()
                if user is not None:
                    user.skills.append(
                        Skills(skill=form.skill.data))
                    
                    db.session.commit()
                    result['savedsuccess'] = True
                else:
                    result['savedsuccess'] = False
            else:
                skill = Skills.query.get(form.skill_id.data)
                form.populate_obj(skill)
                db.session.commit()
                result['savedsuccess'] = True

            return json.dumps(result)

        form.errors['iserror'] = True
        print form.errors
        return json.dumps(form.errors)


    @route('get_skills/<id>')
    @login_required
    def get_skills(self, id):
        skill = Skills.query.get(id)
	print skill._asdict()
        return json.dumps(skill._asdict())


    @route('deleteskills/<id>')
    @login_required
    def deleteskills(self, id):
        skill = Skills.query.get(id)
        db.session.delete(skill)
        db.session.commit()
        result = {}
        result['result'] = 'success';
        return json.dumps(result)    
		
    @route('coursera_update', methods=['POST'])
    @login_required
    def coursera_update(self):        
        form = AddCourseraForm(request.form)        
        result = {}
        if form.validate_on_submit():            
            result['iserror'] = False           
            for entry in form.courseracourses.entries:
                if not entry.data['id']:
                    user = Users.query.filter_by(username=session['username']).first()
                    if user is not None:
                        user.coursera.append(
                            Coursera(coursera_name=entry.data['coursera_nm'], coursera_url=entry.data['coursera_uri']))
                        
                        db.session.commit()
                        result['savedsuccess'] = True
                    else:
                        result['savedsuccess'] = False
                else:
                    course = Coursera.query.get(entry.data['id'])
                    course.coursera_name = entry.data['coursera_nm']
                    course.coursera_url = entry.data['coursera_uri']
                    db.session.commit()
                    result['savedsuccess'] = True

            return json.dumps(result)

        form.errors['iserror'] = True
        print form.errors
        return json.dumps(form.errors)

    @route('coursera_delete', methods=['GET','POST'])
    @login_required
    def coursera_delete(self):
        coursera_id = request.args.get('coursera_id')
        id = request.args.get('id')
        user = Users.query.get(id)
        if user == current_user: 
            course = Coursera.query.get(coursera_id)
            Coursera.query.filter_by(id=coursera_id).delete()
            db.session.commit()
            print id, coursera_id, course
            result = {}
            return json.dumps(result)

    @route('edx_delete', methods=['GET','POST'])
    @login_required
    def edx_delete(self):
        edx_id = request.args.get('edx_id')
        id = request.args.get('id')
        user = Users.query.get(id)
        if user == current_user: 
            edx = Edx.query.get(edx_id)
            Edx.query.filter_by(id=edx_id).delete()
            db.session.commit()
            print id, edx_id, edx
            result = {}
            return json.dumps(result)

    @route('mit_delete', methods=['GET','POST'])
    @login_required
    def mit_delete(self):
        mit_id = request.args.get('mit_id')
        id = request.args.get('id')
        user = Users.query.get(id)
        if user == current_user: 
            mit = MIT.query.get(mit_id)
            MIT.query.filter_by(id=mit_id).delete()
            db.session.commit()
            print id, mit_id, mit
            result = {}
            return json.dumps(result)

    @route('udacity_delete', methods=['GET','POST'])
    @login_required
    def udacity_delete(self):
        udacity_id = request.args.get('udacity_id')
        id = request.args.get('id')
        user = Users.query.get(id)
        if user == current_user: 
            udacity = Udacity.query.get(udacity_id)
            Udacity.query.filter_by(id=udacity_id).delete()
            db.session.commit()
            print id, udacity_id, udacity
            result = {}
            return json.dumps(result)
        
    @route('edx_update', methods=['POST'])
    @login_required
    def edx_update(self):        
        form = AddEDXForm(request.form)        
        result = {}
        if form.validate_on_submit():            
            result['iserror'] = False           
            for entry in form.edxcourses.entries:
                if not entry.data['id']:
                    user = Users.query.filter_by(username=session['username']).first()
                    if user is not None:
                        user.edx.append(
                            Edx(edx_name=entry.data['edx_nm'], edx_url=entry.data['edx_uri']))
                        
                        db.session.commit()
                        result['savedsuccess'] = True
                    else:
                        result['savedsuccess'] = False
                else:
                    course = Edx.query.get(entry.data['id'])
                    course.edx_name = entry.data['edx_nm']
                    course.edx_url = entry.data['edx_uri']
                    db.session.commit()
                    result['savedsuccess'] = True

            return json.dumps(result)

        form.errors['iserror'] = True
        print form.errors
        return json.dumps(form.errors)

    @route('mit_update', methods=['POST'])
    @login_required
    def mit_update(self):        
        form = AddMITForm(request.form)        
        result = {}
        if form.validate_on_submit():            
            result['iserror'] = False           
            for entry in form.mitcourses.entries:
                if not entry.data['id']:
                    user = Users.query.filter_by(username=session['username']).first()
                    if user is not None:
                        user.mit.append(
                            MIT(mit_name=entry.data['mit_nm'], mit_url=entry.data['mit_uri']))
                        
                        db.session.commit()
                        result['savedsuccess'] = True
                    else:
                        result['savedsuccess'] = False
                else:
                    course = MIT.query.get(entry.data['id'])
                    course.mit_name = entry.data['mit_nm']
                    course.mit_url = entry.data['mit_uri']
                    db.session.commit()
                    result['savedsuccess'] = True

            return json.dumps(result)

        form.errors['iserror'] = True
        print form.errors
        return json.dumps(form.errors)

    @route('udacity_update', methods=['POST'])
    @login_required
    def udacity_update(self):        
        form = AddUdacityForm(request.form)        
        result = {}
        if form.validate_on_submit():            
            result['iserror'] = False           
            for entry in form.udacitycourses.entries:
                if not entry.data['id']:
                    user = Users.query.filter_by(username=session['username']).first()
                    if user is not None:
                        user.udacity.append(
                            Udacity(udacity_name=entry.data['udacity_nm'], udacity_url=entry.data['udacity_uri']))
                        
                        db.session.commit()
                        result['savedsuccess'] = True
                    else:
                        result['savedsuccess'] = False
                else:
                    course = Udacity.query.get(entry.data['id'])
                    course.udacity_name = entry.data['udacity_nm']
                    course.udacity_url = entry.data['udacity_uri']
                    db.session.commit()
                    result['savedsuccess'] = True

            return json.dumps(result)

        form.errors['iserror'] = True
        print form.errors
        return json.dumps(form.errors)

ProfileView.register(profile)
