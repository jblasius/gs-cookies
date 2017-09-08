from flask_wtf import Form
from wtforms import SelectMultipleField, SubmitField, widgets, RadioField
from wtforms.validators import DataRequired, Length
from app.models import *


girl_list = [('Amber S.', 'Amber S.'), ('Lindsey B.', 'Lindsey B.'), ('Sierra B.', 'Sierra B.'), ('Olivia R.', 'Olivia R.')]

""" 
https://stackoverflow.com/questions/19564080/how-to-pre-populate-checkboxes-with-flask-wtforms
"""
class ChoiceObj(object):
    def __init__(self, name, choices):
        # this is needed so that BaseForm.process will accept the object for the named form,
        # and eventually it will end up in SelectMultipleField.process_data and get assigned
        # to .data
        setattr(self, name, choices)

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.TableWidget()
    option_widget = widgets.CheckboxInput()

    # uncomment to see how the process call passes through this object
    # def process_data(self, value):
        # return super(MultiCheckboxField, self).process_data(value)

class ColorLookupForm(Form):
    submit = SubmitField('Save')
    colors = MultiCheckboxField(None)

allColors = ( 'red', 'pink', 'blue', 'green', 'yellow', 'purple' )

class GirlChoice(Form):
    girl_choice = RadioField('Name', choices=girl_list)
