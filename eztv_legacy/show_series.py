#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from codecs import open
import json
import tvdb_api

with open('series.json') as f:
    nombre_series = json.loads(f.read())
with open('vistas.json') as f:
    vistas = json.loads(f.read())

def get_next_episode(show, season, episode):
    if season + 1 in show:
        next_aired = show[season + 1][1]['firstaired']
    elif episode + 1 in show[season]:
        next_aired = show[season][episode + 1]['firstaired']
    else:
        next_aired = 'Unknown'

    return next_aired

tv = tvdb_api.Tvdb()
for k, v in vistas.iteritems():
    name = nombre_series[k]
    try:
        show = tv[nombre_series[k]]
        aired = show[v['season']][v['episode']]['firstaired']
        next_aired = get_next_episode(show, v['season'], v['episode'])
    except:
        print("{} not found".format(name))
        aired = 'Unkown'
        next_aired = 'Unknown'

    print("{}: {} -> Season {} Episode {} Date {} Next {}".format(k,
                                                                  name,
                                                                  v['season'],
                                                                  v['episode'],
                                                                  aired,
                                                                  next_aired))
