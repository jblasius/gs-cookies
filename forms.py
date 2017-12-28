from flask_wtf import Form
from wtforms import SubmitField, widgets, RadioField
from wtforms.validators import DataRequired, Length
from app.models import *
from sheet_data import get_girl_names

class GirlChoice(Form):
    girl_names = get_girl_names()

    girl_list = []
    for key, value in girl_names.iteritems():
        girl_list.append([key, key])

    #TODO: Get current girl selection from session/db and make it the default

    girl_choice = RadioField('Name', choices=sorted(girl_list))
