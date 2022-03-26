import json
from datetime import datetime


def sort_shows(shows):
    return sorted(shows, key=lambda k: k.get('priority', 0), reverse=False)


def load_external_conf():
    with open("config.json") as h:
        config = json.loads(h.read())
    return config['config']


def load_title_data(type):
    if type == 1:
        filename = "shows"
    elif type == 2:
        filename = "movies"
    else:
        filename =   "comedies"

    with open('app/templates/{}.json'.format(filename)) as h:
        data = json.loads(h.read())
        titles = []
        for title in data:
            if title['type'] == type:
                titles.append(title)
    return titles


def load_shows_data():
    return load_title_data(1)


def load_movies_data():
    return load_title_data(2)


def load_comedy_data():
    return load_title_data(3)


def write_shows_data(shows, filename):
    with open('app/templates/{}.json'.format(filename), "w")as h:
        json.dump(shows, h)


def update_show(show_name):
    shows = load_shows_data()
    new_shows = []
    max_priority = max([show['priority'] for show in shows])
    for show in shows:
        if show['name'] == show_name:
            swatched = show['season_watched'] + 1
            priority = max_priority + 1
            show_type = show['type']
            new_shows.append({"name": show_name, "season_watched": swatched, "priority": priority, "type": show_type})
        else:
            new_shows.append(show)
    write_shows_data(new_shows)


def add_show_to_list(show_name, season_watched, show_type):
    shows = load_shows_data()

    min_priority = min([show['priority'] for show in shows])
    for show in shows:
        show['priority'] += 1
    new_show = {"name": show_name, "priority": min_priority, "season_watched": season_watched, "type": show_type}
    shows.append(new_show)
    write_shows_data(shows)


def delete_show(name):
    shows = load_shows_data()
    new_shows = []
    for show in shows:
        if show['name'] == name:
            continue
        else:
            new_shows.append(show)
    write_shows_data(new_shows)




