#from gevent import monkey
#monkey.patch_all()

from HTMLParser import HTMLParser
import requests
import gevent


class MyMagnetParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if not hasattr(self, 'magnets'):
            self.magnets = []
        if tag == 'a':
            for name, value in attrs:
                if name == 'href' and value.startswith('magnet'):
                    self.magnets.append(value)


class SearchEngine(object):
    search_url = u'https://thepiratebay.se/search/{}/0/7/0'

    def concurrent_search(self, l):
        jobs = [gevent.spawn(self.search, x) for x in l]
        gevent.joinall(jobs, timeout=10)
        return [job.value for job in jobs]

    def list_search(self, l):
        return [self.search(x) for x in l]

    def search(self, s):
        print("Downloading {}".format(s))
        return self.parse(self.raw_search(s))

    def raw_search(self, s):
        """
        Just return html with magnets based on search string
        """
        url = self.search_url.format(s)
        f = requests.get(url)
        return f.text

    def parse(self, html):
        parser = MyMagnetParser()
        parser.feed(html)
        return parser.magnets
