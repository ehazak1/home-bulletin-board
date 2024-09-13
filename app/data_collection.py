import requests
from utils import load_external_conf, load_shows_data, write_shows_data

def collect_title_meta_data(imdb_id, api_key, type):
    title_api = "https://www.omdbapi.com/?apikey={}&i={}"
    url = title_api.format(api_key, imdb_id)
    r = requests.get(url)
    r_json = r.json()
    print(r_json)
    md = {}
    md['image'] = r_json['Poster']
    md['plot'] = r_json['Plot']
    md['year'] = r_json['Released']
    if type != 2:
        md['seasons'] = r_json['totalSeasons']
    return md


def update_shows_meta_data(key, shows):
    for show in shows:
        ## check if we need to collect data
        if "plot" not in show.keys():
            title_md = collect_title_meta_data(show['imdb_id'], key, show['type'])
            show['image'] = title_md['image']
            show['plot'] = title_md['plot']
            show['year'] = title_md['year']
            if show['type'] != 2:
                show['seasons'] = title_md['seasons']
    
    return shows
   


