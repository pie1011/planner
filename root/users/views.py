from operator import methodcaller
import re
from authomatic.adapters import WerkzeugAdapter
from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash

from root.users.forms import LoginForm, RegistrationForm, SettingsForm
from root.users.models import User
from root.users.oauth_config import authomatic

users = Blueprint("users", __name__)


### ----- Register ----- ###
@users.route("/register", methods=["GET", "POST"])
def register():
    """ Register new user """
    logout_user()
    form = RegistrationForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        user = User(
            email=form.email.data,
            username=form.username.data,
            name=form.name.data,
            password_hash=password_hash,
        )
        user.save()
        flash("Hurray! You are now registered.", category="success")
        return login_and_redirect(user)
    return render_template("users/register.html", form=form)



### ----- Login User ----- ###
@users.route("/login", methods=["GET", "POST"])
def login():
    """ Log in the user (non-oauth) """
    logout_user()
    form = LoginForm()
    if form.validate_on_submit():

        # Check log in type (username or email)
        username_or_email = form.username_or_email.data
        if "@" in username_or_email:
            user = User.objects(email=username_or_email).first()
        else:
            user = User.objects(username=username_or_email).first()
        
        # Check for user and correct password
        if user is not None and user.check_password(form.password.data):
            return login_and_redirect(user)
        else:
            flash("Password and username/email combination not found.", category="error")

    return render_template("users/login.html", form=form)



### ----- User Settings ----- ###
@users.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """ User settings """
    form = SettingsForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.name = form.name.data
        current_user.email = form.email.data

        # Create new hash if password changes
        if form.new_pass.data:
            new_hash = generate_password_hash(form.new_pass.data)
            current_user.password_hash = new_hash

        current_user.save()
        flash("Account settings updated successfully!", category="success")
        return redirect(url_for("core.index"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.name.data = current_user.name
        form.email.data = current_user.email


    return render_template("users/settings.html", form=form, can_disconnect=can_oauth_disconnect())







### ----- Log out or delete account ----- ###

@users.route("/logout")
@login_required
def logout():
    """Log out the current user"""
    logout_user()
    flash("You have successfully logged out.", category="success")
    return redirect(url_for("users.login"))

@users.route("/delete_account")
@login_required
def delete_account():
    """Delete current user's account"""
    current_user.delete()
    flash("Account deleted!", category="success")
    return redirect(url_for("core.index"))









### --------------- OAUTH ROUTES --------------- ###


@users.route("/google_oauth")
def google_oauth():
    """Perform google OAuth operations"""
    return oauth_generalized("Google")




def oauth_generalized(oauth_client):
    """Perform OAuth registration, login, or account association"""
    # Get response object for the WerkzeugAdapter.
    response = make_response()
    # Log the user in, pass it the adapter and the provider name.
    result = authomatic.login(WerkzeugAdapter(request, response), oauth_client)
    # If there is no LoginResult object, the login procedure is still pending.
    if not result:
        return response
    # If there is no result.user something went wrong
    if not result.user:
        flash("Login failed, try again with another method.", category="error")
        return redirect(url_for("users.login"))

    # Update user to retrieve data
    result.user.update()

    db_oauth_key = str(oauth_client).lower() + "_id"

    client_name = result.user.name
    client_oauth_id = result.user.id

    # Check if user in database with this OAuth login already exists
    lookup = {db_oauth_key: client_oauth_id}
    user = User.objects(**lookup).first()

    # Should only enter this block if adding another OAuth to the account
    # in user settings
    if current_user.is_authenticated:
        # OAuth method is already linked to an account, do nothing
        if user:
            flash(
                f"That {oauth_client} account is already linked with an account. "
                f"Please log in to that account through {oauth_client} and un-link "
                "it from that account to link it to this account.",
                category="danger",
            )
        # Add this OAuth method to current user
        else:
            current_user[db_oauth_key] = client_oauth_id
            current_user.save()
        # Should only get here from "settings" so return there
        return redirect(url_for("users.settings"))

    # Register a new user with this OAuth authentication method
    if not user:
        # Generate a unique username from client's name found in OAuth lookup
        base_username = client_name.lower().split()[0]
        username = base_username
        attempts = 0
        while True:
            user = User.objects(username=username).first()
            if user:
                attempts += 1
                username = base_username + str(attempts)
            else:
                break
        # Create user and save to database
        user_data = {
            "username": username,
            "name": client_name,
            db_oauth_key: client_oauth_id,
        }
        user = User(**user_data)
        user.save()
        flash("Thanks for registering!", category="success")

    # Else user was found and is now authenticated
    # Log the found-or-created user in
    return login_and_redirect(user)
    



## ----- DISCONNECTION ----- ##

def can_oauth_disconnect():
    """ Determine if disconnecting is allowed """
    has_gg = True if current_user.google_id else False
    has_email = True if current_user.email else False
    has_pw = True if current_user.password_hash else False

    oauth_count = [has_gg].count(True)
    return bool(oauth_count > 1 or (has_email and has_pw))


def oauth_disconnect(oauth_client):
    """ Disconnect from whatever service is connected """
    if not current_user.is_authenticated:
        return redirect(url_for("users.login"))

    db_oauth_key = str(oauth_client).lower() + "_id"

    current_user[db_oauth_key] = None
    current_user.save()

    flash(f"Disconnected from {oauth_client}!")
    return redirect(url_for("users.settings"))





### --------------- HELPER ROUTES --------------- ###



def login_and_redirect(user):
    """ Welcomes and redirects logged in user """
    login_user(user)
    flash(f"Welcome {user.username}! You are now logged in.", category="success")
    return redirect(url_for("core.index"))