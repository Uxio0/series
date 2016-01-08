#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from lib.seriesDatabase import seriesDatabase
import tvdb_api


bd = seriesDatabase()
tv = tvdb_api.Tvdb()
while True:
    nombre = raw_input("Serie?\n")
    if not nombre:
        break
    show = tv[nombre]
    if not show:
        print("Not found {}\n".format(nombre))
        continue
    answer = raw_input(u"Add %s (y/n)\n" % show.data['seriesname']).lower()
    if answer in ('s', 'y'):
        season = int(raw_input("Season: "))
        episode = int(raw_input("Episode: "))
        bd.insert_serie(show.data['seriesname'], season, episode)
