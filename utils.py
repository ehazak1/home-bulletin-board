import json


def load_external_conf():
    with open("config.json") as h:
        config = json.loads(h.read())
    return config


def create_viewed_images_file(filename):
    with open(filename, 'w') as f:
        empty_list = []
        f.write(json.dumps(empty_list))



