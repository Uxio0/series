#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from seriesDatabase import seriesDatabase


bd = seriesDatabase()
nombre = raw_input("Serie?\n")
while nombre:
    nombre = nombre.lower()
    answer = raw_input(u"Add %s (y/n)\n" % nombre).lower()
    if answer in ('s', 'y'):
        season = int(raw_input("Season: "))
        episode = int(raw_input("Episode: "))
        bd.insert_serie(nombre, season, episode)
        nombre = raw_input("Serie?\n")
