from searchEngine import SearchEngine


class KickAss(SearchEngine):
    search_url = u'https://kat.al/usearch/{}/'


if __name__ == "__main__":
    #print(u'\n').join(pb.search('fifa'))

    ka = KickAss()
    toSearch = ('fifa', 'lego', 'batman',
                'star wars', 'Dragon ball', 'nice', 'ok', 'fine')

    #print([x[0] for x in ka.concurrent_search(toSearch) if x])
    print([x[0] for x in ka.list_search(toSearch) if x])
