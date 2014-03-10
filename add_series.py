#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import codecs
import json

with codecs.open('series.json') as f:
    nombre_series = json.loads(f.read())    
with codecs.open('vistas.json') as f:
    vistas = json.loads(f.read())

nombre = raw_input("Serie?\n")
while nombre:
    for id_serie, serie in nombre_series.iteritems():
        if nombre.lower() in serie.lower():
            answer = raw_input(u"Add %s\n" % serie)
            if answer == 's':
                season = int(raw_input("Season: "))
                episode = int(raw_input("Episode: "))
                vistas[id_serie] = {"season": season,
                                    "episode": episode}
    nombre = raw_input("Serie?\n")

print json.dumps(vistas, indent=4)
with codecs.open('vistas.json', 'wb', encoding='utf-8') as f:
    f.write(json.dumps(vistas, indent=4))
