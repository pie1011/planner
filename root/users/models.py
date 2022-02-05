# User model
from flask_login import UserMixin
from werkzeug.security import check_password_hash

from root.globals import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """ Load user object from session stored id """
    return User.objects(pk=user_id).first()


## User model
class User(db.Document, UserMixin):
    """ User model """
    username = db.StringField(required=True, unique=True, max_length=40, index=True)
    name = db.StringField(required=False, max_length=80, index=True)
    email = db.EmailField(unique=True, required=False, sparse=True, max_length=80, index=True)
    password_hash = db.StringField(required=False, index=True)


    # OAuth info
    google_id = db.StringField(unique=True, required=False, sparse=True, index=True)


    def __repr(self):
        """ User object print format """
        return f"Username: {self.username} id: {self.id}"

    def check_password(self, password):
        """ Check password to hash """
        return check_password_hash(self.password_hash, password)