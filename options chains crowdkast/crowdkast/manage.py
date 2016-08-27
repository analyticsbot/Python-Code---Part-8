from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os
from linkedupapp.config import *
from linkedupapp import application, db

if os.environ['CONFIG_VARIABLE'] == "config.DevelopmentConfig":
        application.config.from_object(config.DevelopmentConfig)
elif os.environ['CONFIG_VARIABLE'] == "config.ProductionConfig":
        application.config.from_object(config.ProductionConfig)

#application.config.from_object(DevelopmentConfig)

migrate = Migrate(application, db)
manager = Manager(application)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
