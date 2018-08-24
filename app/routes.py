from app import app
from flask import render_template, redirect, request, url_for
from app.forms import WatchForm
import json
from random import choice


def load_external_conf():
    with open("config.json") as f:
        config = json.loads(f.read())
    return config


@app.route('/index')
@app.route('/')
def index():
    with open('image_list.lst') as h:
        images = json.loads(h.read())
    image_to_show = choice(images)
    return render_template('index.html', image=image_to_show)


@app.route('/calendar')
def calendar():
    config = load_external_conf()
    calendar_url = config['google_calendar']
    return render_template('calendar.html', calendar_url=calendar_url, port=config['tcp_port'])


@app.route('/showsBacklog', methods=['GET', 'POST'])
def shows_backlog():
    config = load_external_conf()
    form = WatchForm()
    if form.validate_on_submit():
        #show_id, show_name, show_last_season = form.data.values()
        print(form.data.values())

    with open('app/templates/shows.json') as h:
        shows = json.load(h)
    shows = sorted(shows, key=lambda k: k.get('priority', 0), reverse=False)
    return render_template('shows_backlog.html', shows=shows, form=form, request=request, port=config['tcp_port'])
