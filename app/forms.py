from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField


class WatchForm(FlaskForm):
    fin_watched_chkbox = BooleanField()
    submit = SubmitField('Update')
