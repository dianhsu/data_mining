import bs4.element
import requests
from bs4 import BeautifulSoup
import yaml
import json

url = 'https://arxiv.org/list/cs/new'
test_url = 'http://export.arxiv.org/api/query?search_query=all:cs&start=0&max_results=100&sortBy=lastUpdatedDate&sortOrder=descending'
res = requests.get(url)

soup = BeautifulSoup(res.text, features='html5lib')
dlpage = soup.find(id='dlpage')
articles = []
cnt = 0
for dt in dlpage.find('dl').children:
    if dt.name == 'dt':
        dd = dt.find_next('dd')
        # print(dt.name, dd.name)
        abspath = dt.find('a', attrs={'title': 'Abstract'})['href']
        link = f'https://arxiv.org{abspath}'
        abstract = dd.find('p', attrs={'class': 'mathjax'}).string
        title = ''
        for tag in dd.find('div', attrs={'class': 'meta'}).div.children:
            if isinstance(tag, bs4.element.NavigableString):
                title += tag
        try:
            articles.append({
                'link': link.strip(),
                'abstract': abstract.strip(),
                'title': title.strip()
            })
            cnt += 1
        except:
            pass
with open('articles.json', 'w') as f:
    f.write(json.dumps(articles))

print(f'success cnt: {cnt}')
