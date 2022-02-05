## custom validators for users
import re
from webbrowser import get

from flask_login import current_user
from wtforms import ValidationError

from root.users.models import User

def safe_string():
    """ Validates that username meets format requirements """

    def validation(form, field):
        string = field.data.lower()
        pattern = re.compile(r"^[a-z0-9_-]+$")
        match = pattern.match(string)
        if not match:
            message = "Username must consist of only letters, numbers, underscores and dashes."
            raise ValidationError(message)
        
    return validation

    
def current_or_unique(message=None):
    """ Validates that field is current user or not in database """

    def validation(form, field):
        kwargs = {field.name: field.data}
        if ( hasattr(current_user, field.name) and getattr(current_user, field.name) == field.data):
            return
        if User.objects(**kwargs).first():
            raise ValidationError(message)
    
    return validation