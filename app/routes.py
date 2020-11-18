from app import app
from flask import render_template, request, url_for, make_response
from flask_api import status
import logging
from .statsCollector import statsCollector
from .helpers import *


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html')


@app.route('/')
@app.route('/<day>')
def index(day=None):
    stats = statsCollector(day)
    last_updated, results = check_stale_data(stats)

    # Get sessions for the day
    display_session = list(results.keys())

    # Get display cookie, and figure out what to do with it
    display = cookie_setup(display_session)
    # Based on display cookie, decide what to show
    res, display_slideshow = make_display_decision(display, display_session, results)
    
    # Create response, and set cookie value
    resp = make_response(render_template('index.html', results=res, slide_show=display_slideshow , day=stats.day))
    resp.set_cookie('display',  str(display))
    resp.set_cookie('cfjc_res_updated', str(last_updated))
    
    return resp


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    content = {'status': 'healthy'}
    return content, status.HTTP_200_OK
