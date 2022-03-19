from app import app
from flask import render_template, request, url_for, redirect, flash
from app.forms import ShowUpdateForm, AddShowForm
import json
from random import choice
from utils import load_shows_data, load_external_conf, update_show, sort_shows, add_show_to_list, delete_show, \
    load_chores_data, day_of_week, hour_of_day, create_viewed_images_file
from pathlib import Path


@app.route('/index', methods=['GET', 'POST'])
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


@app.route('/newindex', methods=['GET'])
def new_backlog():
    return render_template('new_index.html')
    

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

