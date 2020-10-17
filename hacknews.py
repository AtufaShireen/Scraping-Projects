# using bs4 and requests library
from bs4 import BeautifulSoup
from urllib import url
import requests
import re

articles = []
url = requests.get("https://news.ycombinator.com/news").text
soup = BeautifulSoup(url, 'html.parser')
news = soup.find_all('tr', {'class': 'athing'})
print('~~processing~~'.center(45))
for i in news:
    tit = i.find('a', {'class': 'storylink'})
    if tit:
        title = tit.text  # link, title, score, comment
        link = tit['href']
    else:
        title, link = None, None
    vals = i.find_next_sibling('tr')
    scr = vals.find('span', {'class': 'score'})
    if scr:
        score = scr.text.strip()
    else:
        score = '0 points'
    comm = vals.find('a', string=re.compile(r'\d+(&nbsp;|\s)comment(s?)'))  # 96&nsbp;comments
    if comm:
        comment = comm.text.strip()
        comment = comment.replace('\xa0', ' ')
        comm_link = comm['href']
    else:
        comment,comm_link = '0 comments',None
    articles.append(
        {'link': link,
         'title': title,
         'score': score,
         'comments': comment,
         'comments link':comm_link

         }
    )
print(len(articles))
for article in articles:
    print(article)
