# Scraping data using Hacker News API

import requests

articles = []
url = 'https://hacker-news.firebaseio.com/v0'
stories = requests.get(url + '/topstories.json').json()
for story in stories:
    story_url = url + f'/item/{story}.json'
    r = requests.get(story_url)
    story_dict = r.json()
    try:
        link = story_dict['url']
    except:
        link = None
    title = story_dict['title']
    score = story_dict['score']
    try:
        comments = story_dict['descendants']
    except:
        comments = 0
    articles.append({
        'link': link,
        'title': title,
        'score': score,
        'comments': comments
    })

for article in articles:
    print(article)
