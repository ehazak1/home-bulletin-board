from app import app
from flask import render_template, request, url_for, redirect, flash
from app.forms import ShowUpdateForm, AddShowForm
import json
from random import choice
from utils import load_shows_data, load_external_conf, update_show, sort_shows, add_show_to_list, delete_show


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
    return render_template('calendar.html', calendar_url=calendar_url, port=config['tcp_port'],
                           zipcode=config['zipcode'])


@app.route('/showsBacklog', methods=['GET', 'POST'])
def shows_backlog():
    config = load_external_conf()
    form = ShowUpdateForm()

    if request.method == 'POST' and form.validate_on_submit():
        show = form.sname.data
        delete = form.delete.data

        print("Delete:{}".format(delete))
        if len(show) == 0:
            flash("Must choose a show!")
        elif delete:
            delete_show(show)
        else:
            update_show(show)
        return redirect(url_for('shows_backlog'))

    shows = load_shows_data()
    shows = sort_shows(shows)
    return render_template('shows_backlog.html', shows=shows, form=form, request=request, port=config['tcp_port'])


@app.route('/addShow', methods=['GET', 'POST'])
def add_show():
    form = AddShowForm()

    if request.method == 'POST':
        show = form.sname.data
        swatch = form.swatch.data
        show_type = int(form.show_type.data)
        if len(show) == 0:
            flash('No show added, please type show name')
            return redirect(url_for('add_show'))
        elif show_type == 2 and swatch != 0:
            flash("A movie can't have seasons, please set seasons watched to 0")
            return redirect(url_for('add_show'))
        else:
            add_show_to_list(show, swatch, show_type)
        return redirect(url_for('shows_backlog'))

    return render_template('add_show.html', form=form, request=request)
