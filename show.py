#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from gevent import monkey
#monkey.patch_all()
import tvdb_api
import datetime
from lib.seriesDatabase import seriesDatabase

import transmissionrpc
from transmissionrpc.error import TransmissionError

from lib.piratebay import PirateBay
#from lib.kickass import KickAss
SEARCH_ENGINE = PirateBay()

def add_to_transmission(magnet, host='127.0.0.1', port=9091):
    tc = transmissionrpc.Client(host, port=port)
    try:
        tc.add_uri(magnet)
    except TransmissionError:
        print('Duplicated Torrent')


class Show():
    tv = tvdb_api.Tvdb()

    def __init__(self, name):
        self.name = name
        self.tvShow = tv[name]
        self.all_episodes = None

    def get_all_episodes(self):
        if not self.all_episodes:
            show = self.tvShow
            self.all_episodes = [Episode(self,
                                         show[iseason][iepisode])
                                 for iseason in range(1, len(show))
                                 for iepisode in range(1, len(show[iseason]) + 1)]
        return self.all_episodes

    def get_chapters_from(self, season, episode):
        """
           Return every episode of a show from the chapter specified
        """

        show = self.tvShow
        if season not in show:
            return []
        # Gets remaning episodes for current season
        episodes = [show[season][iepisode]
                    for iepisode in range(episode + 1, len(show[season]) + 1)]
        # Get episodes for new seasons
        episodes += [show[iseason][iepisode]
                     for iseason in range(season + 1, len(show))
                     for iepisode in range(1, len(show[iseason]))]
        return [Episode(self, x) for x in episodes]


    def filter_aired_episodes(self, episodes):
        """
        Returns aired episodes to the actual day
        """
        #Set now one day in the past or check download
        now = datetime.datetime.now() - datetime.timedelta(days=1)
        aired_episodes = [episode for episode in episodes if
                          episode.get_first_aired() and
                          datetime.datetime.strptime(episode.get_first_aired(),
                                                     "%Y-%m-%d")
                          <= now]
        return aired_episodes

    def get_last_aired(self):
        aired = self.filter_aired_episodes(self.get_all_episodes())
        if aired:
            return aired[-1]

    def get_next_aired(self):
        all_episodes = self.get_all_episodes()
        last_aired = self.get_last_aired()
        if last_aired:
            index = all_episodes.index(last_aired)
            try:
                return all_episodes[index + 1]
            except:
                return None


class Episode():
    engine = SEARCH_ENGINE
    def __init__(self, show, episode):
        self.show = show
        self.episode = episode

    def get_first_aired(self):
        return self.episode['firstaired']

    def get_season(self):
        return int(self.episode['seasonnumber'])

    def get_episode_number(self):
        return int(self.episode['episodenumber'])

    def format_episode(self):
        season = self.get_season()
        episode_number = self.get_episode_number()
        return u"{} S{:02d}E{:02d}".format(self.show.name, season,
                                           episode_number)
    def get_next_episode(self):
        show = self.show
        if season + 1 in show and 1 in show[season + 1]:
            episode = self.show[season + 1][1]
        elif episode + 1 in show[season]:
            episode = show[season][episode + 1]
        else:
            episode = None
        if episode:
            return Episode(self.show, episode)

    def get_magnet(self):
        return self.engine.search(self.format_episode())

    def __repr__(self):
        return self.format_episode()


def filter_magnets(magnets, query):
    return [magnet for magnet in magnets
            if query.lower() in magnet.lower()]


bd = seriesDatabase()
series = bd.get_series()
tv = tvdb_api.Tvdb()
for serie in series:
    name = serie[0]
    season = serie[1]
    episode_number = serie[2]
    print('-----------------------------------------')
    print(serie)
    print('-----------------------------------------')
    show = Show(name)
    episodes = show.get_chapters_from(season, episode_number)
    if not episodes:
        print('No episodes for ' + name)
        continue
    print('All episodes known: {}'.format(episodes))
    aired_episodes = show.filter_aired_episodes(episodes)
    next_aired = show.get_next_aired()
    if aired_episodes:
        print('Aired: {}'.format(aired_episodes))
    else:
        print("No episodes for " + name)
        if next_aired:
            print("{} will be avaliable on {}".format(
                next_aired,
                next_aired.get_first_aired()))
        continue

    last_aired = show.get_last_aired()
    ok = True
    for aired_episode in aired_episodes:
        magnet_list = aired_episode.get_magnet()
        filtered_magnets = filter_magnets(magnet_list, '1080p')
        magnet = filtered_magnets[0] if filtered_magnets else magnet_list[0]
        try:
            print('Adding to transmission via rpc {}'.format(aired_episode))
            add_to_transmission(magnet)
            print('Downloading {}'.format(aired_episode))
        except:
            ok = False
            break

    if ok and last_aired:
        bd.update_serie(name, last_aired.get_season(),
                        last_aired.get_episode_number())

        date_new = next_aired.get_first_aired() if next_aired else 'Unknown'
        print("{} -> Season {} Episode {} Last Aired Date {} Next {}".format(name,
                                                                             last_aired.get_season(),
                                                                             last_aired.get_episode_number(),
                                                                             last_aired.get_first_aired(),
                                                                             date_new))
