#This file defines forms used to edit models and fields

#Flask imports
from flask.ext.wtf import Form

from werkzeug.security import generate_password_hash,check_password_hash

#WTForms imports
from wtforms import TextField,PasswordField,IntegerField,BooleanField,SelectField
from wtforms.validators import DataRequired,ValidationError
from wtforms.fields import FormField,TextAreaField
from wtforms_components import DateTimeField

#PVS imports
from pvs import util
from pvs.form.vote import MultiCheckboxField
from pvs.model.user import User

#Form used to edit votes
class VoteEditForm(Form):
    title = TextField("Title",validators=[DataRequired(),util.valid_chars])
    description = TextAreaField("Description",validators=[util.valid_chars])
    users = MultiCheckboxField("Users",coerce=str,choices=[],validators=[])
    grade = SelectField("Grade",validators=[],choices=[('none','none'),('9','9'),('10','10'),('11','11'),('12','12'),('all','all')])
    start_time = DateTimeField("Start Time",validators=[DataRequired()])
    end_time = DateTimeField("End Time",validators=[DataRequired()])
    def validate_end_time(form,field):
	if field.data<=form.start_time.data :
	    raise ValidationError('Please enter an ending time after the starting time')
#Form used to edit articles
class NewsEditForm(Form):
    title = TextField("Title",validators=[DataRequired(),util.valid_chars])
    body = TextAreaField("Body")

#Form used to edit labels
class LabelEditForm(Form):
    title = TextField("Label",validators=[DataRequired(),util.valid_chars])


#Form used to edit multicheckboxes
class MultiEditForm(Form):
    title = TextField("Label",validators=[DataRequired(),util.valid_chars])
    choices = TextAreaField("Choices",validators=[DataRequired(),util.valid_chars])
    max_choices=IntegerField("Max Number of Choices",validators=[DataRequired()])

#Form used to edit single select fields
class OptionEditForm(Form):
    title = TextField("Label",validators=[DataRequired(),util.valid_chars])
    choices = TextAreaField("Choices",validators=[DataRequired(),util.valid_chars])

#Form used to edit accounts (Admin)
class UserEditForm(Form):
    username = TextField("Username",validators=[DataRequired(),util.valid_chars])
    password = PasswordField("Password",validators=[DataRequired(),util.valid_chars])
    grade = SelectField("Grade",validators=[],choices=[('9','9'),('10','10'),('11','11'),('12','12')])
    admin=BooleanField("Admin")

#Form used to edit accounts
class AccountEditForm(Form):
    username = TextField("Username",validators=[DataRequired(),util.valid_chars])
    password = PasswordField("Password",validators=[DataRequired(),util.valid_chars])
