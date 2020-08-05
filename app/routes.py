from app import app
from flask import render_template, request, url_for, redirect, flash, make_response
import json
from random import choice
from utils import load_external_conf, create_viewed_images_file
from pathlib import Path
import logging
from .statsCollector import statsCollector

@app.route('/')
@app.route('/<day>')
def index(day=None):
    # Get stat, results, and sessions for the day
    stats = statsCollector(day)
    results = stats.get_daily_results()
    display_session = list(results.keys())

    # Get display cookie, and figure out what to do with it
    display = request.cookies.get('display')
    if display:
        display = int(display)
        display += 1
        if display > len(display_session):
            display = 0
    else:
        display = 0

    # Based on display cookie, decide what to show
    if display < len(display_session):
        res = results[display_session[display]]
        # Skip empty results 
        if len(res[0]['results']) == 0:
            display += 1
            res = results[display_session[display]]
        display_slideshow = False
    else:
        res = None
        display_slideshow = True
    
    # Create response, and set cookie value
    resp = make_response(render_template('index.html', results=res, slide_show=display_slideshow , day=stats.day))
    resp.set_cookie('display',  str(display))
    
    return resp
