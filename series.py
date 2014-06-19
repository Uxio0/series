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


class Magnet(object):
    def __init__(self, serie, magnet):
        self.serie = serie
        detectado = regex.findall(magnet)[0]
        self.season = int(detectado[0])
        self.episode = int(detectado[1])
        self.magnet = magnet
        self.hd = '720p' in magnet

    def __repr__(self):
        return u"{} S{:02d}E{:02d} -> HD={}".format(nombre_series[str(self.serie)],
                                                    self.season, self.episode,
                                                    self.hd)

    def get_key(self):
        return u"{}S{:02d}E{:02d}".format(self.serie,
                                          self.season, self.episode)


if not os.path.isfile(join(dirname, 'series.json')):
    load_series()

if not os.path.isfile(join(dirname, 'vistas.json')):
    print("Add some series first")
    sys.exit(1)

with open(join(dirname, 'series.json')) as f:
    nombre_series = json.loads(f.read())
with open(join(dirname, 'vistas.json')) as f:
    vistas = json.loads(f.read())


def add_to_transmission(magnets, host='127.0.0.1', port=9091):
    tc = transmissionrpc.Client(host, port=port)
    for magnet in magnets:
        tc.add_uri(magnet.magnet)


def get_magnets(serie_id):
    payload = {'SearchString1': '',
               'SearchString': serie_id,
               'search': 'Search'}
    web = requests.post('http://eztv.it/search/', data=payload)
    return [Magnet(serie_id, x.attr.href)
            for x in pq(web.text)('.magnet').items()
            if regex.findall(x.attr.href)]


def remove_duplicates(magnets):
    duplicates = {}
    for magnet in magnets:
        key = magnet.get_key()
        if key in duplicates:
            if not duplicates[key].hd and magnet.hd:
                duplicates[key] = magnet
        else:
            duplicates[key] = magnet

    return duplicates.values()


total_magnets = []
for id_vista, vista in vistas.iteritems():
    id_vista = int(id_vista)
    season = vista['season']
    episode = vista['episode']

    magnets = get_magnets(id_vista)
    if not magnets:
        continue

    to_add = []
    for magnet in magnets:
        if (season < magnet.season or
            (season == magnet.season
             and episode < magnet.episode)):

            total_magnets.append(magnet)
        if magnet.season > vista['season']:
            vista['season'] = magnet.season

        if magnet.episode > vista['episode']:
            vista['episode'] = magnet.episode

    #TODO optimize this
    vista['season'] = max([magnet.season for magnet in magnets])
    vista['episode'] = max([magnet.episode for magnet in magnets if
                            magnet.season == vista['season']])

total_magnets = remove_duplicates(total_magnets)
for magnet in total_magnets:
    print(magnet)

add_to_transmission(total_magnets),
with open(join(dirname, 'vistas.json'), 'wb', 'utf-8') as f:
    f.write(json.dumps(vistas, indent=4))
