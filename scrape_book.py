import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import OrderedDict
import dataset

db = dataset.connect('sqlite:///scrape_quotes.db')


def scrape_books(url):
    print('scraping page:', url)
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    articles = soup.find_all('article', class_='product_pod')
    for arts in articles:
        book = arts.find('h3')
        book_tag = book.find('a')
        book_url = urljoin(url, book_tag.get('href'))
        book_name = book_tag.get('title')
        db['book'].upsert({
            'book_name': book_name,
            'book_url': book_url,
            'updated': datetime.now()
        },['book_name'])


def scrape_book(url):
    new_book = OrderedDict()
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    main = soup.find(class_='product_main')
    title = main.find('h1').get_text(strip=True)
    price = main.find(class_='price_color').get_text(strip=True)
    stock = main.find(class_='availability').get_text(strip=True)
    rating = ' '.join(main.find(class_='star-rating').get('class')).replace('star-rating', '').strip()
    img = soup.find(class_='thumbnail').find('img').get('src')
    description = soup.find(id='product_description')
    desc = ''
    if description:
        desc = description.find_next_sibling('p').get_text(strip=True)
    new_book['title'] = title
    new_book['price'] = price
    new_book['stock'] = stock
    new_book['rating'] = rating
    new_book['img'] = img
    new_book['description'] = desc

    table_info = soup.find(string='Product Information').find_next('table')
    rows = table_info.find_all('tr')
    for row in rows:
        header = row.find('th').get_text(strip=True)
        # Since we'll use the header as a column, clean it a bit
        # to make sure SQLite will accept it
        header = re.sub('[^a-zA-Z]+', '_', header)
        value = row.find('td').get_text(strip=True)

        new_book[header] = value
    print('---------book dict: ', new_book)

    db['book_info'].upsert(new_book,['book_name'])


base_url = 'http://books.toscrape.com/'
url = base_url
while True:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    scrape_books(url)
    next_page = soup.find('li', class_='next').find('a')
    next_page = next_page.get('href')
    if next_page is None:
        break
    url = urljoin(url, next_page)
    p = input('Scrape next page?')
    if p == 'y':
        continue
    else:
        break
x = db['book'].find(order_by=['last_seen'])
print(x)
for row in x:
    print('scraping, ', row)
    print(row['book_name'])
    scrape_book(row['book_url'])
    # updating last seen to now,
    db['books'].upsert({'book_name':row['book_name'],'last_seen':datetime.now()},['book_name'])
