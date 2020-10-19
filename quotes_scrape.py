import requests
import dataset
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3

conn = sqlite3.connect('scrape_quotes.db')
cur = conn.cursor()
# db = dataset.connect('sqlite:///quote.db') with dataset

cur.execute('''
CREATE TABLE IF NOT EXISTS Quotes(
p_id INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
quote TEXT,
author TEXT
)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Tags(
id AUTO INCREMENT PRIMARY KEY,
quote_id BIGINT,
tag TEXT
)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Author(
id AUTO INCREMENT PRIMARY KEY,
name TEXT,
born TEXT,
description TEXT
);
''')
conn.commit()
# Tables with these data
# quotes,tags, authors
# quotes ->  quotes, author
# tags -> quote id, tag
# authors -> id, author, born date+ loc, desc

author_urls = set()


def get_quotes(soup):
    quotes_tag = soup.find_all('div', {'class': 'quote'})
    for quotes in quotes_tag:
        quote = quotes.find('span', {'class': 'text'}).text.strip()  # quote
        # print('quote:', quote)
        tags = quotes.find_all('a', {'class': 'tag'})  # tags for a quote
        tag = [i.text.strip() for i in tags]
        # print([i for i in tag])
        auth = quotes.find('small', {'class': 'author'})
        author = auth.text.strip()  # author name
        # print('author:', author)
        link = auth.find_next_sibling('a').get('href')
        auth_link = urljoin(base, link)
        # print('author link: ', auth_link)
        author_urls.add(auth_link)

        # storing this data
        # quote_id = db['quotes'].insert({'text': quote, 'author': author})  with dataset
        cur.execute('''
        INSERT INTO Quotes (quote, author) VALUES (?,?)''', (quote, author,)
                    )

        # print('quote id:', quote_id)
        # db['quote_tags'].insert_many(
        #     [{'quote_id': quote_id, 'tag_id': tg} for tg in tag] with dataset
        # )
        conn.commit()
        x = cur.execute('SELECT p_id FROM Quotes WHERE quote = (?)', (quote,)).fetchone()[0]
    
        tgs = [(tg, x) for tg in tag]

        cur.executemany('''
                INSERT INTO Tags (quote_id, tag) VALUES (?,?)''', tgs
                        )

        conn.commit()


def scrape_author(author_id):
    r = requests.get(author_id).text
    soup = BeautifulSoup(r, 'html.parser')
    name_tag = soup.find('div', class_='author-details')
    print('scraping author page: ', author_id)
    name = name_tag.find('h3', class_='author-title').text.strip()
    # print('name ', name)
    born_tag = name_tag.find('p').find_all('span')
    born = ' '.join([i.text for i in born_tag])
    desc = soup.find('div', class_='author-description').text.strip()

    cur.execute('''INSERT INTO Author (name, born, description) VALUES (?,?,?)''', (name, born, desc))
    conn.commit()

    # db['authors'].insert({'name': name,       with dataset
    #                       'born': born,
    #                       'description': desc})


base = 'http://quotes.toscrape.com/'
url = base
while True:
    print('scraping page: ', url)
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    get_quotes(soup)
    next_page = soup.find('li', class_='next').find('a')
    if next_page is None:
        break
    new_url = next_page.get('href')
    url = urljoin(base, new_url)
for auth_id in author_urls:

    scrape_author(auth_id)


conn.close()
