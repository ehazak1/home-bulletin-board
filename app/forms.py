from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, IntegerField, BooleanField
from utils import load_shows_data


class ShowUpdateForm(FlaskForm):
    shows = load_shows_data()
    choices = [(show['name'], show['name']) for show in shows]
    choices.append(('', ''))
    sname = SelectField('Show', choices=sorted(choices))
    delete = BooleanField()
    submit = SubmitField()


class AddShowForm(FlaskForm):
    sname = StringField()
    swatch = IntegerField()
    submit = SubmitField()

