import os
import os.path
import sqlite3


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class seriesDatabase():
    c = None

    def __init__(self):
        file_path = os.path.join(__location__, 'series.db')
        self.c = sqlite3.connect(file_path)
        self.c.row_factory = sqlite3.Row
        try:
            self.c.execute('''CREATE TABLE shows
                           (name text UNIQUE, season integer, episode integer,
                           date timestamp)''')
        except sqlite3.OperationalError:
            return

        self.c.commit()

    def insert_serie(self, name, season, episode):
        if season < 1:
            season = 1
        if episode < 1:
            episode = 0
        try:
            self.c.execute(u"INSERT INTO SHOWS VALUES(?,?,?,CURRENT_TIMESTAMP)", (name,
                                                                                  season,
                                                                                  episode))

            self.c.commit()
        except sqlite3.IntegrityError:
            pass

    def update_serie(self, name, season, episode):
        if season < 1:
            season = 1
        if episode < 1:
            episode = 0

        self.c.execute(u"UPDATE shows SET season=?,episode=?,date=CURRENT_TIMESTAMP where name=?", (season,
                                                                                                    episode,
                                                                                                    name))
        self.c.commit()

    def get_series(self, name=None):
        query = u"SELECT * FROM shows"
        cursor = self.c.execute(query)
        return cursor.fetchall()
