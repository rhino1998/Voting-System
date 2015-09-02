#This file defines the Form and Fields for voting

#Flask imports
from flask.ext.wtf import Form

#PVS imports
from pvs import util

#WTForms imports
from wtforms import TextField,PasswordField
from wtforms.fields import SelectMultipleField, FormField
from wtforms.validators import DataRequired
from wtforms.widgets import ListWidget,CheckboxInput

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()
    def __init__(self,label=None,
        validators=None,
        filters=(),
        description=u'',
        id=None,
        default=None,
        _form=None,
        _name=None,
        _prefix='',
        _translations=None,
        coerce=unicode,
        choices=[],
        max_choices=0
    ):
	self.max_choices=max_choices
	super(MultiCheckboxField,self).__init__(
            label=label,
            validators=validators,
            filters=filters,
            description=description,
            id=id,
            default=default,
            _form=_form,
            _name=_name,
            _prefix=_prefix,
            _translations=_translations,
            choices=choices,
            coerce=coerce
        )

class VoteForm(object):
    """#Defines a class that creates a dynamic class with custom attributes
    """
    def __init__(self):
    	self.fields=[]
    def get(self):
	return type('DynamicForm',(Form,),{(''.join(('id_',str(i)))):field for i,field in enumerate(self.fields)})()




