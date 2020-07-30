from app import app
from flask import render_template, request, url_for, redirect, flash
import json
from random import choice
from utils import load_external_conf, create_viewed_images_file
from pathlib import Path
import logging


@app.route('/index')
@app.route('/')
def index():
    # Read configuration
    with open("config.json") as f:
        config = json.loads(f.read())
    images_list_file = config['picture_frame']['image_list']
    viewed_images_file = config['picture_frame']['viewed_image_list']

    # Open image list
    with open(images_list_file) as h:
        images = json.loads(h.read())

    #Create viewed image list if one doesn't exist
    if not Path(viewed_images_file).is_file():
        create_viewed_images_file(viewed_images_file)

    # Clean up viewed images if needed
    with open(viewed_images_file) as f:
        viewed_images = json.loads(f.read())
        if len(viewed_images) == len(images):
            viewed_images = []
            create_viewed_images_file(viewed_images_file)

    # Select image to display
    for image_to_show in images:
        if image_to_show[0] in viewed_images:
            continue
        viewed_images.append(image_to_show[0])
        with open(viewed_images_file, 'w') as f:
            f.write(json.dumps(viewed_images))
        break

    return render_template('index.html')
