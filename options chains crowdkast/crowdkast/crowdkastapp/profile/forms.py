from flask.ext.wtf import Form
from wtforms import TextField,FieldList, PasswordField, validators, HiddenField, TextAreaField, BooleanField, FormField, StringField
from wtforms.validators import Required, EqualTo, Optional, Length, Email

			
class SkillForm(Form):
    skill_id = HiddenField()
    skill = TextField('Enter your skills', validators=[
            validators.Length(min = 2, message=(u'The skill should should have at least 2 characters'))
            ])
		
class CourseraForm(Form):    
    id = HiddenField()
    coursera_nm = (TextField('Enter the course name', validators=[
            validators.Length(min = 0, message=('Length should be at least 4 characters'))
            ]))
    coursera_uri = (TextField('Enter the course url', validators=[
            validators.Length(min = 0, message=('Length should be at least 10 characters'))
            ]))
    def __init__(self, *args, **kwargs):
            kwargs['csrf_enabled'] = False
            super(CourseraForm, self).__init__(*args, **kwargs)

class AddCourseraForm(Form):
	courseracourses = FieldList(FormField(CourseraForm), min_entries=1)
	
class EDXForm(Form):
    id = HiddenField()
    edx_nm = TextField('Enter your edx course name', validators=[
            validators.Length(min = 0, message=())
            ])
    edx_uri = TextField('Enter your edx course url', validators=[
            validators.Length(min = 0, message=())
            ])
    def __init__(self, *args, **kwargs):
            kwargs['csrf_enabled'] = False
            super(EDXForm, self).__init__(*args, **kwargs)

class AddEDXForm(Form):
	edxcourses = FieldList(FormField(EDXForm), min_entries=1)
	
class MITForm(Form):
    id = HiddenField()
    mit_nm = TextField('Enter your MIT course name', validators=[
            validators.Length(min = 0, message=())
            ])
    mit_uri = TextField('Enter your MIT course url', validators=[
            validators.Length(min = 0, message=())
            ])
    def __init__(self, *args, **kwargs):
            kwargs['csrf_enabled'] = False
            super(MITForm, self).__init__(*args, **kwargs)

class AddMITForm(Form):
	mitcourses = FieldList(FormField(MITForm), min_entries=1)

    
class UdacityForm(Form):
    id = HiddenField()
    udacity_nm = TextField('Enter your Udacity course name', validators=[
            validators.Length(min = 0, message=())
            ])
    udacity_uri = TextField('Enter your Udacity course url', validators=[
            validators.Length(min = 0, message=())
            ])
    def __init__(self, *args, **kwargs):
            kwargs['csrf_enabled'] = False
            super(UdacityForm, self).__init__(*args, **kwargs)

class AddUdacityForm(Form):
	udacitycourses = FieldList(FormField(UdacityForm), min_entries=1)

