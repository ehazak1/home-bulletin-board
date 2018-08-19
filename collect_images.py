import requests
import json


API_BASE_URL = "https://api.smugmug.com/api/v2/"


def fix_img_url(url):
    url_broken = url.split('/')
    url_broken[-1] = url_broken[-1].replace('Th', 'XL')
    url_broken[-2] = url_broken[-2].replace('Th', 'XL')
    return "/".join(url_broken)


def main():
    with open("config.json") as f:
        config = json.loads(f.read())
    api_key = config['smugmug']['smugmug_api_key']
    user = config['smugmug']['smugmug_user']
    headers = {'Accept': 'application/json'}
    # figure out how many albums we have today
    request_url = "{}user/{}!albums?APIKey={}".format(API_BASE_URL, user, api_key)
    r = requests.get(request_url, headers=headers)
    r.close()
    count = json.loads(r.text)['Response']['Pages']['Total']
    albums_url = "{}&start=1&count={}".format(request_url, count)
    r = requests.get(albums_url, headers=headers)
    r.close()
    album_list = list()
    for album in json.loads(r.text)['Response']['Album']:
        album_list.append(album['AlbumKey'])

    image_list = list()
    # Get all the images from each album
    n = 1
    for album_key in album_list:
        album_images_base_uri = "https://api.smugmug.com/api/v2/album/{}!images?APIKey={}".format(album_key, api_key)
        print("Collecting images from: {} ({}/{})".format(album_key, n, len(album_list)))
        r = requests.get(album_images_base_uri, headers=headers)
        try:
            image_list_response = json.loads(r.text)['Response']['AlbumImage']
        except KeyError:
            n += 1
            continue
        for image in image_list_response:
            image_list.append(fix_img_url(image['ThumbnailUrl']))
        n += 1

    with open("image_list.lst", "w") as h:
        h.write(json.dumps(image_list))


if __name__ == "__main__":
    main()
