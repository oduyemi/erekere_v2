from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, length, Regexp
# from ereapp.models import User, Admin, Contact

    


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), length(min=3, max=40)],
        render_kw={"placeholder": "Username"}
    )
    
    password = PasswordField(
        "Password",
        validators=[DataRequired(), length(min=5, max=20)],
        render_kw={"placeholder": "Enter your password"}
    )

    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class SignUp(FlaskForm):
    fullname = StringField(
        "Fullname",
        validators=[DataRequired(), length(min=3, max=100)],
        render_kw={"placeholder": "Fullname"}
    )

    phone = StringField(
        "Phone",
        validators=[DataRequired(), length(min=7, max=15)],
        render_kw={"placeholder": "Phone Number"}
    )

    username = StringField(
        "Username",
        validators=[DataRequired(), length(min=3, max=40)],
        render_kw={"placeholder": "Username"}
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), length(min=5, max=20)],
        render_kw={"placeholder": "Password"}
    )

    submit = SubmitField("Sign Up")
