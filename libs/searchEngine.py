#from gevent import monkey
#monkey.patch_all()

from HTMLParser import HTMLParser
import requests
requests.packages.urllib3.disable_warnings()
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

    def __init__(self, verify=False):
        #Verify SSL Cert
        self.verify = verify

    def concurrent_search(self, l):
        jobs = [gevent.spawn(self.search, x) for x in l]
        gevent.joinall(jobs, timeout=10)
        return [job.value for job in jobs]

    def list_search(self, l):
        return [self.search(x) for x in l]

    def search(self, s):
        return self.parse(self.raw_search(s))

    def raw_search(self, s):
        """
        Just return html with magnets based on search string
        """
        url = self.search_url.format(s)
        f = requests.get(url, verify=self.verify)
        return f.text

    def parse(self, html):
        parser = MyMagnetParser()
        parser.feed(html)
        return parser.magnets
