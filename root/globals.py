## Separate file to avoide infinite import loops

from distutils.log import Log
from flask_login import LoginManager
from flask_mongoengine import MongoEngine

# Database
db = MongoEngine()

# Login manager
login_manager = LoginManager()