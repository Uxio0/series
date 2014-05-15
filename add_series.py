#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from codecs import open
import json

with open('series.json') as f:
    nombre_series = json.loads(f.read())

try:
    f = open('vistas.json')
    vistas = json.loads(f.read())
except IOError:
    vistas = {}

nombre = raw_input("Serie?\n")
while nombre:
    for id_serie, serie in nombre_series.iteritems():
        if nombre.lower() in serie.lower():
            answer = raw_input(u"Add %s\n" % serie).lower()
            if answer in ('s', 'y'):
                season = int(raw_input("Season: "))
                episode = int(raw_input("Episode: "))
                vistas[id_serie] = {"season": season,
                                    "episode": episode}
    nombre = raw_input("Serie?\n")

print json.dumps(vistas, indent=4)
with open('vistas.json', 'wb', encoding='utf-8') as f:
    f.write(json.dumps(vistas, indent=4))
