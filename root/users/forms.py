from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

from root.users.custom_form_validators import safe_string, current_or_unique


class RegistrationForm(FlaskForm):
    """ Register new users """

    email = StringField(
        "Email",
        description="email@email.com",
        validators=[
            DataRequired(),
            Email(),
            current_or_unique("Email provided is already registered."),
        ],
    )
    username = StringField(
        "Username",
        description="Username",
        validators=[
            DataRequired(),
            current_or_unique("Username is unavailable."),
            safe_string(),
            Length(min=3, max=40),
        ],
    )
    name = StringField(
        "Your Name",
        description="Your Name",
        validators=[
            DataRequired(),
            Length(min=1, max=80),
        ],
    )
    password = PasswordField(
        "Password",
        description="Old Password",
        validators=[
            DataRequired(),
            Length(min=5, max=40),
        ],
    )
    pass_confirm = PasswordField(
        "Confirm Password",
        description="Password confirm",
        validators=[
            DataRequired(),
            EqualTo("pass_confirm", message="Passwords do not match!"),
        ],
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    """ Log in without oauth """

    username_or_email = StringField(
        "Username or email",
        description="Username or email",
        validators=[DataRequired()],
    )
    password = PasswordField(
        "Password", description="Password", validators=[DataRequired()]
    )
    submit = SubmitField("Log In")




## ----- Settings Form ------ ##
class SettingsForm(FlaskForm):
    """ User settings """

    email = StringField(
        "Email",
        description="email@email.com",
        validators=[
            DataRequired(),
            Email(),
            current_or_unique("Email provided is already registered."),
        ],
    )
    username = StringField(
        "Username",
        description="Username",
        validators=[
            DataRequired(),
            current_or_unique("Username is unavailable."),
            safe_string(),
            Length(min=3, max=40),
        ],
    )
    name = StringField(
        "Your Name",
        description="Your Name",
        validators=[
            Optional(),
            Length(min=1, max=80),
        ],
    )
    new_pass = PasswordField(
        "New Password",
        description="Old Password",
        validators=[
            Optional(),
            Length(min=5, max=40),
        ],
    )
    pass_confirm = PasswordField(
        "Confirm Password",
        description="Password confirm",
        validators=[
            Optional(),
            EqualTo("pass_confirm", message="Passwords do not match!"),
        ],
    )
    submit = SubmitField("Update")
