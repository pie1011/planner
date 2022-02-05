# Testing OAuth setup
from authomatic.adapters import WerkzeugAdapter
from flask import Flask, make_response, request

from root.users.oauth_config import authomatic

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <p><a href="/users/google_oauth">Go to Google</a></p>
    """

@app.route("/users/google_oauth")
def google_oauth():
    return oauth_generalized("Google")


def oauth_generalized(oauth_client):
    """Generalized OAuth data retrieval"""

    # Response object for WerkzeugAdapter
    response = make_response()

    # Log in, pass adapter and provider
    result = authomatic.login(WerkzeugAdapter(request, response), oauth_client)

    if not result:
        return response
    
    if not result.user:
        return "Failed to retrieve OAuth user"
    
    # Update user to retrieve data
    result.user.update()

    # Return dictionary of user data, converted to JSON automatically by Flask
    return result.user.data


if __name__ == "__main__":
    # Initiate app
    app.run()