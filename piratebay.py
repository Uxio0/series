from gevent import monkey
monkey.patch_all()

import urllib2
from HTMLParser import HTMLParser
import gevent


class MyMagnetParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if not hasattr(self, 'magnets'):
            self.magnets = []
        if tag == 'a':
            for name, value in attrs:
                if name == 'href' and value.startswith('magnet'):
                    self.magnets.append(value)


class PirateBay():
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
        url = u'https://thepiratebay.se/search/{}/0/7/0'.format(s)
        f = urllib2.urlopen(url)
        return f.read()

    def parse(self, html):
        parser = MyMagnetParser()
        parser.feed(html)
        return parser.magnets


if __name__ == "__main__":
    #print(u'\n').join(pb.search('fifa'))

    pb = PirateBay()
    toSearch = ('fifa', 'lego', 'batman',
                'star wars', 'Dragon ball', 'nice', 'ok', 'fine')

    print([x[0] for x in pb.concurrent_search(toSearch) if x])
