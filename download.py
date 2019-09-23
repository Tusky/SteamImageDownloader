import json
import re
import sys
import os
import urllib.request
import datetime
from urllib.error import HTTPError

steam_db_file = 'data.json'
steam_db = {}


def initialize_db():
    exists = os.path.exists(steam_db_file)
    day_old = False
    if exists:
        created_at = os.path.getmtime(steam_db_file)
        day_old = datetime.datetime.fromtimestamp(created_at) + datetime.timedelta(hours=24) <= datetime.datetime.now()
    if not exists or day_old:
        get_steam_db()
    load_database()


def get_steam_db():
    print('Downloading recent Steam App DB.')
    url = f'http://api.steampowered.com/ISteamApps/GetAppList/v0002/'
    urllib.request.urlretrieve(url, steam_db_file)


def load_database():
    print('Loading Steam App DB from cache.')
    with open(steam_db_file, encoding='UTF-8') as json_file:
        data = json.load(json_file)
        apps = data.get('applist', {}).get('apps', [])
        for app in apps:
            steam_db[str(app['appid'])] = convert_name(app['name'])


def convert_name(name: str):
    return re.sub('[^a-zA-Z0-9]', '', name)


def get_app_name(steam_id):
    return steam_db[steam_id]


def download_header(steam_id):
    print(f'Downloading header image for {get_app_name(steam_id)}')
    url = f'https://steamcdn-a.akamaihd.net/steam/apps/{steam_id}/header.jpg'
    urllib.request.urlretrieve(url, f'{get_app_name(steam_id)}_header.jpg')


def download_library(steam_id):
    print(f'Downloading Library image for {get_app_name(steam_id)}')
    url = f'https://steamcdn-a.akamaihd.net/steam/apps/{steam_id}/library_600x900.jpg'
    portrait_url = f'https://steamcdn-a.akamaihd.net/steam/apps/{steam_id}/portrait.png'
    try:
        urllib.request.urlretrieve(url, f'{get_app_name(steam_id)}_library.jpg')
    except HTTPError:
        print(f'Couldn\'t Library image. Downloading Portrait image instead for {get_app_name(steam_id)}')
        urllib.request.urlretrieve(portrait_url, f'{get_app_name(steam_id)}_portrait.png')


if __name__ == '__main__':
    initialize_db()
    steam_ids = sys.argv[1:]
    for steam_id in steam_ids:
        download_header(steam_id)
        download_library(steam_id)
        print(f'--- Finished downloading images for {get_app_name(steam_id)}.')
