import json


def sort_shows(shows):
    return sorted(shows, key=lambda k: k.get('priority', 0), reverse=False)


def load_external_conf():
    with open("config.json") as h:
        config = json.loads(h.read())
    return config


def load_shows_data():
    with open('app/templates/shows.json') as h:
        return json.loads(h.read())


def write_shows_data(shows):
    with open('app/templates/shows.json', "w")as h:
        json.dump(shows, h)


def update_show(show_name):
    shows = load_shows_data()
    new_shows = []
    max_priority = max([show['priority'] for show in shows])
    for show in shows:
        if show['name'] == show_name:
            swatched = show['season_watched'] + 1
            priority = max_priority + 1
            new_shows.append({"name": show_name, "season_watched": swatched, "priority": priority})
        else:
            new_shows.append(show)
    write_shows_data(new_shows)


def add_show_to_list(show_name, season_watched):
    shows = load_shows_data()

    min_priority = min([show['priority'] for show in shows])
    for show in shows:
        show['priority'] += 1
    new_show = { 'name': show_name, 'priority': min_priority, 'season_watched': season_watched }
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




