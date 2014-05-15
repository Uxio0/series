import urllib2
from pyquery import PyQuery as pq
import json
from codecs import open


def load_series():
    r = urllib2.Request('https://eztv.it/search/',
                        headers={'User-Agent': "Magic Browser"})
    r = urllib2.urlopen(r)
    p = pq(r.read())

    series = p("select").children()[1:]
    series_d = {}
    for serie in series:
        serie = pq(serie)
        series_d[serie.attr("value").strip()] = serie.text().strip()

    with open('series.json', 'wb', 'utf-8') as f:
        f.write(json.dumps(series_d, indent=4))

    return series_d

if __name__ == '__main__':
    for k, v in load_series().iteritems():
        print("{} -> {}".format(k, v))
