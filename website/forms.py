from flask_wtf import FlaskForm
from flask import Flask
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired

# creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    name=StringField("User Name", validators=[InputRequired(), DataRequired()])
    emailid = StringField("Email Address", validators=[Email("Please enter a valid email"),DataRequired()])
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match"), DataRequired()])
    password_hash = PasswordField("Confirm Password")
    contact_number=StringField("Contact Number", validators=[InputRequired(), DataRequired()])
    street_address=StringField("Street Address", validators=[InputRequired(), DataRequired()])

    # submit button
    submit = SubmitField("Register")

