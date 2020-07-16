from app import app
from flask import render_template, request, url_for, redirect, flash
import json
from random import choice
from utils import load_external_conf, create_viewed_images_file
from pathlib import Path


@app.route('/index')
@app.route('/')
def index():
    with open("config.json") as f:
        config = json.loads(f.read())
    images_list_file = config['picture_frame']['image_list']
    viewed_images_file = config['picture_frame']['viewed_image_list']

    with open(images_list_file) as h:
        images = json.loads(h.read())

    if not Path(viewed_images_file).is_file():
        create_viewed_images_file(viewed_images_file)

    with open(viewed_images_file) as f:
        viewed_images = json.loads(f.read())
        if len(viewed_images) == len(images):
            viewed_images = []
            create_viewed_images_file(viewed_images_file)

    for image_to_show in images:
        if image_to_show in viewed_images:
            continue
        viewed_images.append(image_to_show)
        with open(viewed_images_file, 'w') as f:
            f.write(json.dumps(viewed_images))
        break

    return render_template('index.html', image=image_to_show)
