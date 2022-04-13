from distutils.command.config import config
import re
from app import app
from flask import render_template, request, url_for, redirect, flash
#from app.forms import ShowUpdateForm, AddShowForm, MovieUpdateForm, ComedyUpdateForm
from app.forms import ShowUpdateForm, AddShowForm
from random import choice
from utils import load_shows_data, load_external_conf, update_show, sort_shows, add_show_to_list, delete_title, \
     load_movies_data, load_comedy_data, write_shows_data, content_type_to_filename, create_choices
from app.data_collection import update_shows_meta_data
from pathlib import Path
#from requests_toolbelt import MutlipartEncoder 


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def shows():
    config = load_external_conf()
    form = ShowUpdateForm()
    shows = load_shows_data()
    form.sname.choices = create_choices(shows)

    if request.method == 'POST' and form.validate_on_submit():
        title = form.sname.data
        delete = form.delete.data
        print("Delete:{}".format(delete))
        if len(title) == 0:
            flash("Must choose a show!")
        elif delete:
            delete_title(title)
        else:
            update_show(title)
        return redirect(url_for('shows'))

    
    shows = update_shows_meta_data(config['imdb_key'], shows)
    write_shows_data(shows, "shows")
    shows = sort_shows(shows)
    return render_template('index.html', shows=shows, form=form, page_type="Show")
    

@app.route('/movies', methods=['GET', 'POST'])
def movies():
    config = load_external_conf()
    form = ShowUpdateForm()
    movies = load_movies_data()
    form.sname.choices = create_choices(movies)

    if request.method == 'POST' and form.validate_on_submit():
        title = form.sname.data
        delete = form.delete.data

        print("Delete:{}".format(delete))
        if len(title) == 0:
            flash("Must choose a Movie!")
        elif delete:
            delete_title(title)
        else:
            update_show(title)
        return redirect(url_for('movies'))

    
    movies = update_shows_meta_data(config['imdb_key'], movies)
    write_shows_data(movies, "movies")
    movies = sort_shows(movies)
    
    return render_template('index.html', shows=movies, form=form, page_type="Movie")


@app.route('/comedies', methods=['GET', 'POST'])
def comedies():
    config = load_external_conf()
    form = ShowUpdateForm()
    comedies = load_comedy_data()
    form.sname.choices = create_choices(comedies)

    if request.method == 'POST' and form.validate_on_submit():
        title = form.sname.data
        delete = form.delete.data

        print("Delete:{}".format(delete))
        if len(title) == 0:
            flash("Must choose a show!")
        elif delete:
            delete_title(title)
        else:
            update_show(title)
        return redirect(url_for('comedies'))

    comedies = update_shows_meta_data(config['imdb_key'], comedies)
    write_shows_data(comedies, "comedies")
    comedies = sort_shows(comedies)
    return render_template('index.html', shows=comedies, form=form, page_type="Comedy")


@app.route('/addContent', methods=['GET', 'POST'])
def add_content():
    form = AddShowForm()

    if request.method == 'POST':
        show = form.sname.data
        swatch = form.swatch.data
        show_type = int(form.show_type.data)
        imdb_id = form.imdb_id.data
        streaming_service = form.streaming_service.data
        if len(show) == 0:
            flash('No show added, please type show name')
            return redirect(url_for('add_content'))
        elif show_type == 2 and swatch != 0:
            flash("A movie can't have seasons, please set seasons watched to 0")
            return redirect(url_for('add_content'))
        else:            
            add_show_to_list(show, swatch, show_type, imdb_id, streaming_service)
        return redirect(url_for('{}'.format(content_type_to_filename(show_type))))

    return render_template('add_content.html', form=form, request=request)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

'''
@app.route('/download', method=['GET'])
def download():
    m = MutlipartEncoder({
        'shows.json': 
    })
'''
