#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from codecs import open
import json
import tvdb_api

with open('series.json') as f:
    nombre_series = json.loads(f.read())
with open('vistas.json') as f:
    vistas = json.loads(f.read())

tv = tvdb_api.Tvdb()
for k, v in vistas.iteritems():
    show = tv[nombre_series[k]]
    aired = show[v['season']][v['episode']]['firstaired']
    print("{} -> Season {} Episode {} Date {}".format(nombre_series[k],
                                                      v['season'],
                                                      v['episode'],
                                                      aired))
