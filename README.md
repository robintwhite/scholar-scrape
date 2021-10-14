# scholar-scrape

# update scholarly
Add the method to scholarly class in _scholarly

def search_pubs_url(self, url):
    " Given specific URL related to publication search terms, perform scrape"
    return self.__nav.search_publications(url)
