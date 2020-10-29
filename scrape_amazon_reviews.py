from selenium import webdriver
from bs4 import BeautifulSoup
import pandas
from urllib.parse import urlparse
from collections import defaultdict

DRIVER_PATH = r'C:\Users\HP\PycharmProjects\mylogger\chromedriver\chromedriver.exe'
url = 'https://www.amazon.com/Learning-Python-Allen-Downey/product-reviews/9351198146/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber=1'

options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument('--disable-extensions')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

all_stars = []
all_rev = []


def scrape(soup):
    data_tg = soup.find_all('div', {'data-hook': 'review'})
    print(len(data_tg))

    for data in data_tg:
        try:
            stars = data.find('i', {'data-hook': 'cmps-review-star-rating'})  # cmps for .com
            star = float(stars.text.strip().split(' ')[0])
            all_stars.append(star)
        except:
            stars = 0.0
            print('n stars found', stars)
            all_stars.append(stars)
        try:
            review = data.find('span', {'data-hook': 'review-title'})
            rev = review.text.strip()
            all_rev.append(rev)

        except:
            review = 'No reviews'
            all_rev.append(review)


while True:
    driver.get(url)
    content = driver.page_source
    print('page path',urlparse(url).path)
    page = urlparse(url).query.split('&pageNumber=')[1]
    print('page part 1', page)
    page = page.split('&')[0]
    print('page part 2', page)
    filename = (urlparse(url).path).split('/')[1] + str(page) + '.html'
    print(filename)

    with open(filename, 'w', encoding='UTF-8') as f:  # saving the data for reuse without buffer
        cont = f.write(content)

    soup = BeautifulSoup(content, 'html.parser')
    print('scraping next page')
    scrape(soup)
    next_page = soup.find('li', class_='a-last')
    try:
        next_page = next_page.a.get('href')
        print(next_page)
        url = 'https://www.amazon.com' + next_page
        print('next url', url)
    except:
        print('Finished Scraping')
        break


def to_frame(data):  # filters out common reviews
    df = pandas.Series(data).to_frame('amazon').reset_index()
    df.columns = ['Review', 'Star']
    print('----Data Frame---')
    print(df.head)


def to_dataframe(x, y):
    df = pandas.DataFrame({'Reviews': x, 'Stars': y})
    print(df.head)
    df.to_csv('Reviews.csv')


print(len(all_rev))
# x = defaultdict(zip(all_rev, all_stars))  pass to to_frame

to_dataframe(all_rev, all_stars)  # convert to csv and and data frame
