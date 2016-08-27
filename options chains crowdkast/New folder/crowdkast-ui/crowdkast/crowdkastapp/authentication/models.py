from collections import OrderedDict
from crowdkastapp import db


class Users(db.Model, object):

    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    fname = db.Column(db.String(101))
    lname = db.Column(db.String(101))
    password = db.Column(db.String(255))
    email = db.Column(db.String(100), unique=True)

    registered_on = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)

    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    name = db.Column(db.String(60))
    oauth_token = db.Column(db.String(200))
    oauth_secret = db.Column(db.String(200))

    mode_signup = db.Column(db.Integer)

    
       
    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result



