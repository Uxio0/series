#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from codecs import open
import json

with open('series.json') as f:
    nombre_series = json.loads(f.read())
with open('vistas.json') as f:
    vistas = json.loads(f.read())

for k, v in vistas.iteritems():
    print("{} -> Season {} Episode {}".format(nombre_series[k],
                                              v['season'],
                                              v['episode']))
