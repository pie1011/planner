import os
from datetime import datetime

from bson import ObjectId, json_util
from flask import Flask
from flask.json import JSONEncoder

from root.core.views import core
from root.globals import db, login_manager
from root.users.views import users

class MongoJsonEncoder(JSONEncoder):
    """Adjustments to the flask json encoder for MongoEngine support"""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)


# Create the app!
def create_app():
    """ Create the app! """

    app = Flask(__name__)
    app.json_encoder = MongoJsonEncoder

    # Update config with env variables
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["MONGODB_SETTINGS"] = {
        "db": os.getenv("AUTHENTICATION_SOURCE"),
        "authentication_source": os.getenv("AUTHENTICATION_SOURCE"),
        "host": os.getenv("MONGODB_HOST"),
        "port": int(os.getenv("MONGODB_PORT")),
        "username": os.getenv("MONGODB_USERNAME"),
        "password": os.getenv("MONGODB_PASSWORD")
    }

    # Blueprints registration
    app.register_blueprint(core, url_prefix="")
    app.register_blueprint(users, url_prefix="/users")

    # Database initialization
    db.init_app(app)

    # Login manager initialization
    login_manager.init_app(app)
    login_manager.login_view = "users.login"

    return app