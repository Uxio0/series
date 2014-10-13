#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()
import tvdb_api
import datetime
from seriesDatabase import seriesDatabase
from piratebay import PirateBay


def get_next_episode(show, season, episode):
    if season + 1 in show:
        next_aired = show[season + 1][1]['firstaired']
    elif episode + 1 in show[season]:
        next_aired = show[season][episode + 1]['firstaired']
    else:
        next_aired = 'Unknown'

    return next_aired


def get_show_from_tvdb(serie, tv=None):
    if not tv:
        tv = tvdb_api.Tvdb()

    name = serie['name']
    episode = serie['episode']
    season = serie['season']
    show = tv[name]
    episodes = [show[season][iepisode]
                for iepisode in range(episode, len(show[season]))]
    # This fix chapter number for new season
    episodes += [show[iseason][iepisode]
                 for iseason in range(season + 1, len(show))
                 for iepisode in range(1, len(show[iseason]))]
    return episodes


def get_aired_episodes(episodes):
    #Set now one day in the past or check download
    now = datetime.datetime.now() - datetime.timedelta(days=1)
    aired_episodes = [episode for episode in episodes if
                      datetime.datetime.strptime(episode['firstaired'],
                                                 "%Y-%m-%d")
                      <= now]
    return aired_episodes


def format_episode(name, episode):
    season = int(episode['seasonnumber'])
    episode = int(episode['episodenumber'])
    return u"{} S{:02d}E{:02d}".format(name, season,
                                       episode)


def get_magnets(episodes, engine):
    return engine.concurrent_search(episodes)


def filter_magnets(magnets, query):
    return [magnet for magnet in magnets
            if query.lower() in magnet.lower()]


if __name__ == "__main__":
    bd = seriesDatabase()
    bd.insert_serie('The Walking Dead', 1, 2)
    bd.update_serie('The Walking Dead', 4, 2)
    bd.insert_serie('The Walking Dead', 1, 2)
    print(bd.get_series())

series = bd.get_series()
tv = tvdb_api.Tvdb()
pb = PirateBay()
for serie in series:
    episodes = get_show_from_tvdb(serie, tv)
    aired_episodes = get_aired_episodes(episodes)
    last_aired = aired_episodes[-1]
    last_aired_index = episodes.index(last_aired)
    if (len(episodes) - 1) > last_aired_index:
        next_aired = episodes[last_aired_index + 1]
    else:
        next_aired = 'Unknown'

    magnets = get_magnets([format_episode(serie['name'], aired_episode) for
                           aired_episode in aired_episodes],
                          pb)
    filtered_magnets = [filter_magnets(magnet_list, '1080p')
                        for magnet_list in magnets]
    print([filtered[0] for filtered in filtered_magnets
           if len(filtered)])

    #print(episodes)
    #print(aired_episodes)
    print("{} -> Season {} Episode {} Last Aired Date {} Next {}".format(serie['name'],
                                                                         serie['season'],
                                                                         serie['episode'],
                                                                         last_aired['firstaired'],
                                                                         next_aired['firstaired']))
