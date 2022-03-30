import requests
from utils import load_external_conf, load_shows_data, write_shows_data

def collect_title_meta_data(imdb_id, api_key, type):
    title_api = "https://imdb-api.com/en/API/Title/{}/{}"
    url = title_api.format(api_key, imdb_id)
    r = requests.get(url)
    r_json = r.json()
    md = {}
    md['image'] = r_json['image']
    md['plot'] = r_json['plot']
    if type == 2:
        md['year'] = r_json['year']
    else:
        md['year'] = "{}-{}".format(r_json['year'], r_json['tvSeriesInfo']['yearEnd'])
        md['seasons'] = len(r_json['tvSeriesInfo']['seasons'])
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
   


