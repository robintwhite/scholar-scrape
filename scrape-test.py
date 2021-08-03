# %% Imports
import numpy as np 
import pandas as pd 
from scholarly import scholarly
from utils import scholar
import os
import time
import random
import requests, bs4
from tqdm import tqdm
# %% Get search terms from file
search_terms = []
with open("search_terms.txt") as f:
    lines = f.readlines()
    for line in lines:
        search_terms.append(line.strip())

# %% Test publication search using scholarly
sq = scholar.ScholarQuery()
phrase = sq._parenthesize_phrases(f'{search_terms[1]}, Robin White')
print(phrase)
# %%
search_query = scholarly.search_pubs(query=phrase,
                                    patents=True, 
                                    citations=True,
                                    year_low=2018, 
                                    year_high=None,
                                    sort_by='relevance')

article = next(search_query)
scholarly.pprint(article)

# %% Possible search query inputs. Maybe read from json file for user input
words = None # The default search behavior
words_some = None # At least one of those words
words_none = None # None of these words
phrase = None #
scope_title = False # If True, search in title only
author = None
pub = None
timeframe = [None, None]
include_patents = True
include_citations = True

# %% Create url using scholar utils with more advanced search options
ssq = scholar.SearchScholarQuery()
ssq.set_words('Zeiss, "Xradia Versa"') #can set more than one and with quotations for exact phrase
#ssq.set_phrase('Xradia Versa') #specific phrase
ssq.set_timeframe(start=None, end=None)
url = ssq.get_url()
print(url)

# %% Get total number of articles for query
def get_num_results(url):
    ''' Return the total number of results from the search query url. Taken from scholar.py'''
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text)
    tag = soup.find(name='div', attrs={'id': 'gs_ab_md'})
    if tag is not None:
        raw_text = tag.findAll(text=True)
        # raw text is a list because the body contains <b> etc
        if raw_text is not None and len(raw_text) > 0:
            try:
                num_results = raw_text[0].split()[1]
                # num_results may now contain commas to separate
                # thousands, strip:
                num_results = num_results.replace(',', '')
                return int(num_results)
            except (IndexError, ValueError):
                print('Error') 
                pass

# %% 
num_results = get_num_results(url)
print(num_results)

# %%
url_scholarly = url.replace('http://scholar.google.com','') # call to url in scholarly 'https://scholar.google.com{0}'

if num_results:
    article_list = []
    search_query = scholarly.search_pubs_url(url_scholarly)
    for _ in tqdm(range(num_results)):
        try:
            article = next(search_query)
            # scholarly.pprint(article)
            article_list.append(article)
            time.sleep(random.uniform(0,1)) # random sleep for google
        except StopIteration:
            print('No more results to show')
            continue
else:
    print(f'No results to show: {num_results}')

# %%
print(len(article_list))
scholarly.pprint(article_list[0])

# %% Pandas database - get values
col_titles = ['authors', 'author_ids', 'title', 'abstract', 'pub_year', 'journal',
                'citations', 'eprint_url', 'pub_url', 'citedby_url', 'scilab_url', 
                'related_articles_url', 'scholarbib_url']

authors = []
author_ids = []
paper_titles = []
abstracts = []
year = []
journals = []
citations = []
eprint_urls = []
pub_urls = []
citedby_urls = []
scilab_urls = []
related_articles_urls = []
scholarbib_urls = []

for article in tqdm(article_list):
    authors.append(article['bib'].get('author', ''))

    author_ids.append(article.get('author_id', ''))

    paper_titles.append(article['bib'].get('title', ''))

    abstracts.append(article['bib'].get('abstract', ''))

    year.append(article['bib'].get('pub_year', ''))

    journals.append(article['bib'].get('venue', ''))

    citations.append(article.get('num_citations', ''))

    eprint_urls.append(article.get('eprint_url', ''))

    pub_urls.append(article.get('pub_url', ''))

    citedby_urls.append(article.get('citedby_url', ''))

    scilab_urls.append(article.get('url_add_sclib', ''))

    related_articles_urls.append(article.get('url_related_articles', ''))

    scholarbib_urls.append(article.get('url_scholarbib',''))


# %% Pendas Database - create dataframe
df = pd.DataFrame({
    'authors': authors,
    'author_ids': author_ids,
    'title': paper_titles,
    'abstract': abstracts,
    'pub_year': year,
    'journal': journals,
    'citations': citations,
    'eprint_url': eprint_urls,
    'pub_url': pub_urls,
    'citedby_url': citedby_urls,
    'scilab_url': scilab_urls,
    'related_articles_url': related_articles_urls,
    'scholarbib_url': scholarbib_urls})
# %%
# Scrape citation url for exact author list, and journal 

# %%
# import pickle
# pickle.dump(article_list, open( "test_article_list.p", "wb" ) )

# %%
# Can create separate query for specific authors with more information and articles 