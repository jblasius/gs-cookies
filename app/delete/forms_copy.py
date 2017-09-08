from flask_wtf import Form
from wtforms import SelectMultipleField, SubmitField, widgets, RadioField
from wtforms.validators import DataRequired, Length
from app.models import *


# """
# http://wtforms.readthedocs.io/en/latest/widgets.html#custom-widgets
# """
# def select_multi_checkbox(field, ul_class='', **kwargs):
#     kwargs.setdefault('type', 'checkbox')
#     field_id = kwargs.pop('id', field.id)
#     html = [u'<ul %s>' % html_params(id=field_id, class_=ul_class)]
#     for value, label, checked in field.iter_choices():
#         choice_id = u'%s-%s' % (field_id, value)
#         options = dict(kwargs, name=field.name, value=value, id=choice_id)
#         if checked:
#             options['checked'] = 'checked'
#         html.append(u'<li><input %s /> ' % html_params(**options))
#         html.append(u'<label for="%s">%s</label></li>' % (field_id, label))
#     html.append(u'</ul>')
#     return u''.join(html)


# field = (
#     ['Amber S.', 'Amber S.', "False"],
#     ['Sierra B.', 'Sierra B.', "False"],
#     ['Lindsey B.', 'Lindsey B.', "True"]
#     )

girl_list = [('Amber S.', 'Amber S.'), ('Lindsey B.', 'Lindsey B.'), ('Sierra B.', 'Sierra B.'), ('Olivia R.', 'Olivia R.')]

"""
https://gist.github.com/doobeh/503819eff1661cff612d
http://stackoverflow.com/questions/13558345/flask-app-using-wtforms-with-selectmultiplefield
"""
# class ChooseGirlForm(Form):
#     # choose_girl = SelectMultipleField(
#     #     'Pick Things!',
#     #     choices=data,
#     #     option_widget=widgets.CheckboxInput(),
#     #     widget=widgets.ListWidget(prefix_label=False)
#     #     )

#     choose_girl = SelectMultipleField(
#         u'Choose which girl(s) are associated with your account',
#         choices=girl_list,
#         option_widget=widgets.CheckboxInput(),
#         widget=widgets.ListWidget(prefix_label=False)
#         )


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

class GirlLookupForm(Form):
    submit = SubmitField('Save')
    girls = MultiCheckboxField(None)

class GirlChoice(Form):
    girl_choice = RadioField('Label', choices=girl_list)
