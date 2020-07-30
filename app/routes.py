from app import app
from flask import render_template, request, url_for, redirect, flash
import json
from random import choice
from utils import load_external_conf, create_viewed_images_file
from pathlib import Path
import logging
from .statsCollector import statsCollector


@app.route('/index')
@app.route('/')
def index():
    stats = statsCollector()
    results = stats.get_daily_results()

    return render_template('index.html', results=results, slide_show=False, day=stats.day   )
