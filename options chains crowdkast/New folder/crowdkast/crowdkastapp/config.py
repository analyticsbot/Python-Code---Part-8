import os
	
## default config
class BaseConfig(object):
    DEBUG = True
    CSRF_ENABLED = True
    SECRET_KEY = '\x9bM&l\xbe.\x9f\x15"\xe2\xd836\xb4\xb8\xad\xbd\xb87^\x0b\xe99\x9f'
    WTF_CSRF_SECRET_KEY  = "jajajajaja"
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "static", "upload")
    ALLOWED_EXTENSIONS = set(['bmp', 'png', 'jpg', 'jpeg', 'gif'])
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = '6LexDw8TAAAAAL1vA_EdIeShJQT_8xM5-nehsCzd'
    RECAPTCHA_PRIVATE_KEY = '6LexDw8TAAAAAMqMtYgBi-5XCb7-0jLs0D__2H-Z'
    RECAPTCHA_OPTIONS = {'theme': 'white'}
    SECURITY_PASSWORD_SALT = 'my_precious_two'

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
##    MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
##    MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']
    MAIL_USERNAME = 'ivar.dodo123@gmail.com'
    MAIL_PASSWORD = 'ravihari!12'

    # mail accounts
    MAIL_DEFAULT_SENDER = 'from@example.com'

    FACEBOOK_APP_ID = '956730041029725'
    FACEBOOK_APP_SECRET = '89c69bd08ffb5c6d1978aff785a0e59a'

    CONSUMER_KEY = 'N2sIVsie0TYvsEi36ezemjBnn'
    CONSUMER_SECRET = 'IpKMAK3hCPBPvFg5w6D4mYI0pVdS4R5ZWbcKVKYvhB728VR9X8'


## local config
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://crowdkast:crowdkast@localhost:5432/crowdkast'

## production config
class ProductionConfig(BaseConfig):
    DEBUG = True	
    try:
        SQLALCHEMY_DATABASE_URI = os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL')+'/linkedup'
    except:
        pass
