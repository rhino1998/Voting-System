#This file defines user forms

#Flask imports
from flask.ext.wtf import Form

#PVS imports
from pvs import util
from pvs.model.user import User,UserKey

#WTForms
from wtforms import TextField,PasswordField,IntegerField,SelectField
from wtforms.validators import DataRequired,ValidationError

#Form for login
class LoginForm(Form):
    username = TextField("Username",validators=[DataRequired(message="Please enter a username")])
    password = PasswordField("Password",validators=[DataRequired(message="Please enter a password")])

#Form for registration
class RegisterForm(Form):
    key = TextField("Registration Key",validators=[DataRequired(),util.valid_chars])
    username = TextField("Username",validators=[DataRequired(),util.valid_chars])
    password = PasswordField("Password",validators=[DataRequired(),util.valid_chars])
    grade = SelectField("Grade",validators=[],choices=[('9','9'),('10','10'),('11','11'),('12','12')])
    def validate_key(form,field):
	if UserKey.query.filter_by(key=(field.data)).first() is None:
		raise ValidationError('Enter a valid key')
    def validate_username(form,field):
	if User.query.filter_by(username=(field.data)).first() is not None:
		raise ValidationError('That username is taken')
#Form to create keys
class KeyCreateForm(Form):
    keys=IntegerField("Number of keys",validators=[DataRequired()])
