from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, length

class UserForm(FlaskForm):
    username=StringField("Username", validators=[InputRequired(), length(max=20, message="Username is too long, it must be 20 characters or less")])
    password=PasswordField("Password", validators=[InputRequired()])
    email=EmailField("Email", validators=[InputRequired(), length(max=50, message="Email is too long, try a shorter one")])
    first_name=StringField("First Name", validators=[InputRequired(), length(max=30, message="First name is too long, try abbreviating it")])
    last_name=StringField("Last Name", validators=[InputRequired(), length(max=30, message="Last name is too long, try abbreviating it")])

class LoginForm(FlaskForm):
    username=StringField("Username", validators=[InputRequired(), length(max=20, message="Username is too long, it must be 20 characters or less")])
    password=PasswordField("Password", validators=[InputRequired()])
    

class FeedbackForm(FlaskForm):
    title=StringField("Title", validators=[InputRequired(), length(max=100, message="Titles must be 100 characters or less")])
    content = TextAreaField("Feedback Text", validators=[InputRequired()] ) 