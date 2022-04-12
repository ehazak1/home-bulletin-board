from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, IntegerField, BooleanField, RadioField
from utils import load_movies_data, load_shows_data, load_comedy_data


class ShowUpdateForm(FlaskForm):
    shows = load_shows_data()
    sname = SelectField('Show', choices=[])
    delete = BooleanField()
    submit = SubmitField()


class AddShowForm(FlaskForm):
    sname = StringField()
    swatch = IntegerField()
    show_type = SelectField('Type', choices=sorted([(1, 'Show'), (2, 'Movie'), (3, 'Comedy')]))
    imdb_id = StringField()
    streaming_service = RadioField('', choices=['Netflix', 'Amazon Prime', 'Disney+', 'HBO Max', 'AppleTV+', 'Hulu', 'Starz',
    'Showtime'])
    submit = SubmitField()
    
