import requests
from bs4 import BeautifulSoup
import re

session = requests.Session()


def login_git():
    data = {}
    url = 'https://github.com/{}'
    r = session.get(url.format('login')).text
    soup = BeautifulSoup(r, 'html.parser')
    form = soup.find('form')

    for i in form.select('input[type=hidden]'):
        data[i.get('name')] = i.get('value')
    data.update({'login': '<UserName>', 'password': '<Github Password>'})
    print('logging in with this data', data)
    r = session.post(url.format('session'), data=data)
    # Get the profile page
    r = session.get(url.format(user))
    html_soup = BeautifulSoup(r.text, 'html.parser')

    user_info = html_soup.find('ul', class_='vcard-details')
    print(user_info.text)


def scrape_repo(repos):
    for i in repos:
        try:
            name = i.find('a', {'itemprop': 'name codeRepository'}).text.strip()
        except:
            name = 'No Title'
        try:
            desc = i.find('p', {'itemprop': 'description'}).text.strip()
        except:
            desc = 'No description specified'
        try:
            lang = i.find('span', {'itemprop': 'programmingLanguage'}).text.strip()
        except:
            lang = 'no language specified'

        try:
            stars = i.find('a', {'href': re.compile(r'\/stargazers')}).text.strip()
        except:
            stars = '0'
        print('Title:', name, 'stars:', stars, 'language: ', lang)
        print('description:', desc)
        print()
    print()


login_git()
user = 'macuyiko'
url = f'https://github.com/{user}?tab=repositories'

r = session.get(url)
print(r.text)
soup = BeautifulSoup(r.text, 'html.parser')
while True:
    repos = soup.find_all('li', {'itemprop': 'owns'})
    scrape_repo(repos)
    next_page = soup.find('a', class_='next_page')
    user_next_page = soup.find('a', string='Next')
    if next_page:
        next_page = next_page.get('href')
        url = f'https://github.com{next_page}'
        r = session.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
    elif user_next_page:
        next_page = user_next_page.get('href')
        url = next_page
        r = session.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
    else:
        break
