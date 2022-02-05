# Core views
from flask import Blueprint, render_template

core = Blueprint("core", __name__)

@core.route("/")
def index():
    """ Index page view """
    return render_template("core/index.html")