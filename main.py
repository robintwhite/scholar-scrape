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

# %% Get search terms
sq = scholar.ScholarQuery()
phrase = sq._parenthesize_phrases(",".join(search_terms)) #",".join(search_terms)
print(phrase)

# %% Create url using scholar utils with more advanced search options
ssq = scholar.SearchScholarQuery()
ssq.set_words(phrase) #can set more than one and with quotations for exact phrase
#ssq.set_phrase('Xradia Versa') #specific phrase
ssq.set_timeframe(start=None, end=None)
url = ssq.get_url()
print(url)

# %% Get total number of articles for query
# NOTE: This only works for more than 10 results as the text changes from 'About XX results' to 'XX results'
# Need to fix this to be more robust
def get_num_results(url):
    ''' Return the total number of results from the search query url. Taken from scholar.py'''
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features="lxml")
    tag = soup.find(name='div', attrs={'id': 'gs_ab_md'})
    if tag is not None:
        raw_text = tag.findAll(text=True)
        # raw text is a list because the body contains <b> etc
        if raw_text is not None and len(raw_text) > 0:
            try:
                num_results = raw_text[0].split()[1] # Only for 'About XX results' text
                # num_results may now contain commas to separate
                # thousands, strip:
                num_results = num_results.replace(',', '')
                return int(num_results)
            except (IndexError, ValueError):
                print('Error: Possibly fewer than 1 page of results') 
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
df.to_csv('scholar_scrape.csv')
# %%
# Scrape citation url for exact author list, and journal 

# %%
# import pickle
# pickle.dump(article_list, open( "test_article_list.p", "wb" ) )

# %%
# Can create separate query for specific authors with more information and articles 