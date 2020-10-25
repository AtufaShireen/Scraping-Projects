import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd

session = requests.Session()
url = 'https://www.imdb.com/title/tt6468322/episodes?season={}'
ratings = []
episodes = []

for season in range(1, 6):
    r = session.get(url.format(season))
    soup = BeautifulSoup(r.text, 'html.parser')
    listings = soup.find('div', 'list detail eplist')
    for ep_num, ep in enumerate(listings.find_all('div', recursive=False)):  # direct div tags
        episode = f"{season}/{ep_num + 1}"
        rating_tg = ep.find('span', {'class': 'ipl-rating-star__rating'})
        if rating_tg:
            rating = float(rating_tg.text.strip())
        else:
            rating = 0.0
        print('episode no', episode, '---rating:', rating)
        episodes.append(episode)
        ratings.append(rating)

df = pd.DataFrame({'episodes': episodes, 'ratings': ratings})

df.plot(kind='bar', x='episodes', y='ratings')

plt.show()
