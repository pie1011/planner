import os

from authomatic import Authomatic
from authomatic.providers import oauth2

OAUTH_CONFIG = {
    "Google": {
        "id": 1,
        "class_": oauth2.Google,
        "consumer_key": os.getenv("GOOGLE_ID"),
        "consumer_secret": os.getenv("GOOGLE_SECRET"),
        "scope": ["profile", "email"],
    }
}

# Instantiate Authomatic
authomatic = Authomatic(
    OAUTH_CONFIG,
    os.getenv("AUTHOMATIC_SECRET"),
    report_errors=True, # SET TO FALSE IN PRODUCTION
)