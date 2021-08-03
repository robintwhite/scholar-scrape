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
import pickle
# %% Load pickle - list from initial scrape
article_list = pickle.load(open('test_article_list.p', 'rb'))
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
# %% Pandas Database - create dataframe
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
# %% Get authors and journal info from citation
scholar_base_url = r'https://scholar.google.com/'
# %%
#/html/body/div[1]/table/tbody/tr[5]/td/div/text()
def get_citation_info(url):
    ''' Return the total number of results from the search query url. Taken from scholar.py'''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
                'scheme': 'https',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features='lxml')
    table = soup.find('table')
    data = []
    if table is not None:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append(cols)
    else:
        print('Table not found')
    print(data[4])
# %%
url = scholar_base_url + scholarbib_urls[0]
print(url)
get_citation_info(url)
# %%
