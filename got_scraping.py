import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd

session = requests.Session()
url = 'http://www.imdb.com/title/tt0944947/episodes/?season={}'
ratings = []
episodes = []

for season in range(1, 9):
    r = session.get(url.format(season))
    print('url,', r)
    soup = BeautifulSoup(r.text, 'html.parser')
    listings = soup.find('div', 'list detail eplist')
    for ep_num, ep in enumerate(listings.find_all('div', recursive=False)):  # direct div tags
        episode = f"{season}/{ep_num + 1}"
        rating_tg = ep.find('span', {'class': 'ipl-rating-star__rating'})
        rating = float(rating_tg.text.strip())
        print('episode no', episode, '---rating:', rating)
        episodes.append(episode)
        ratings.append(rating)

df = pd.DataFrame({'episodes': episodes, 'ratings': ratings})

df.plot(kind='bar', x='episodes', y='ratings')


plt.show()
