#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from codecs import open
import json
from pyquery import PyQuery as pq
import re
import requests
import transmissionrpc
import os.path
from os.path import join
import sys

from load_series import load_series

regex = re.compile(r"S(\d{2})E(\d{2})")
dirname = os.path.dirname(os.path.realpath(__file__))

if not os.path.isfile('series.json'):
    load_series()

if not os.path.isfile('vistas.json'):
    print("Add some series first")
    sys.exit(1)

with open(join(dirname, 'series.json')) as f:
    nombre_series = json.loads(f.read())
with open(join(dirname, 'vistas.json')) as f:
    vistas = json.loads(f.read())


def add_to_transmission(torrents, host='127.0.0.1', port=9091):
    tc = transmissionrpc.Client(host, port=port)
    for torrent in torrents:
        tc.add_uri(torrent)


def get_magnets(serie_id):
    payload = {'SearchString1': '',
               'SearchString': serie_id,
               'search': 'Search'}
    web = requests.post('http://eztv.it/search/', data=payload)
    return [x.attr.href for x in pq(web.text)('.magnet').items()]


def format_season(season, episode):
    return u"S%02iE%02i" % (season, episode)


def remove_duplicates(magnets):
    duplicates = {}
    for magnet in magnets:
        detected = regex.findall(magnet)
        if detected:
            is_720 = '720' in magnet
            detected = ''.join(detected[0])
            if detected in duplicates:
                if not duplicates[detected]['720'] and is_720:
                    duplicates[detected]['magnet'] = magnet
                    duplicates[detected]['720'] = True
            else:
                duplicates[detected] = {'magnet': magnet,
                                        '720': is_720}

    return [x['magnet'] for x in duplicates.itervalues()]


#First magnets in eztv are the recent ones
#So we iterate the list until we find our
#chapter
total_magnets = []
for id_vista, vista in vistas.iteritems():
    id_vista = int(id_vista)
    season = vista['season']
    episode = vista['episode']

    magnets = get_magnets(id_vista)
    if not magnets:
        continue

    #Removing the good but not interesting right now Pirate bay movie
    if magnets[0] == 'magnet:?xt=urn:btih:79816060EA56D56F2A2148CD45705511079F9BCA&tr=udp://tracker.openbittorrent.com:80/':
        magnets = magnets[1:]

    to_add = []
    for magnet in magnets:
        detectado = regex.findall(magnet)
        if detectado:
            detectado = detectado[0]
        else:
            continue
        detected_season = int(detectado[0])
        detected_episode = int(detectado[1])
        if detectado:
            if (vista['season'] < detected_season or
                (vista['season'] == detected_season
                 and vista['episode'] < detected_episode)):

                vista['season'] = detected_season
                vista['episode'] = detected_episode
                vista['episode'] = detected_episode

            if (season < detected_season or
                (season == detected_season
                 and episode < detected_episode)):
                print u"Adding {} {}x{}".format(nombre_series[str(id_vista)],
                                                detected_season,
                                                detected_episode)
                to_add.append(magnet)

    total_magnets += remove_duplicates(to_add)


add_to_transmission(total_magnets),
with open(join(dirname, 'vistas.json'), 'wb', 'utf-8') as f:
    f.write(json.dumps(vistas, indent=4))
