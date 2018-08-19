from app import app
from flask import render_template, redirect, request
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


@app.route('/calender')
def calender():
    config = load_external_conf()
    calender_url = config['google_calendar']
    return render_template('calender.html', calender_url=calender_url, port=config['tcp_port'])


@app.route('/showsBacklog', methods=['GET', 'POST'])
def shows_backlog():
    config = load_external_conf()
    form = WatchForm()
    if form.validate_on_submit():
        app.logger.debug("I'm in the showsBacklog Page")

    with open('app/templates/shows.json') as h:
        shows = json.load(h)
    shows = sorted(shows, key=lambda k: k.get('priority', 0), reverse=False)
    return render_template('shows_backlog.html', shows=shows, form=form, request=request, port=config['tcp_port'])
