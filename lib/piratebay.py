from searchEngine import SearchEngine


class PirateBay(SearchEngine):
    search_url = u'https://pirateproxy.vip/search/{}/0/7/0'


if __name__ == "__main__":
    #print(u'\n').join(pb.search('fifa'))

    pb = PirateBay()
    toSearch = ('fifa', 'lego', 'batman',
                'star wars', 'Dragon ball', 'nice', 'ok', 'fine')

    print([x[0] for x in pb.concurrent_search(toSearch) if x])
