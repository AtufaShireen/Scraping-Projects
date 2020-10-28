from selenium import webdriver
from bs4 import BeautifulSoup
import pandas
from urllib.parse import urlparse

DRIVER_PATH = r'C:\Users\HP\PycharmProjects\mylogger\chromedriver\chromedriver.exe'
url = 'https://www.amazon.com/Learning-Python-Allen-Downey/product-reviews/9351198146/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'

options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument('--disable-extensions')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get(url)
content = driver.page_source
filename = (urlparse(url).path).split('/')[1] + '.html'
print(filename)
with open(filename, 'w', encoding='UTF-8') as f:  # saving the data for reuse without buffer
    cont = f.write(content)

soup = BeautifulSoup(content, 'html.parser')
data_tg = soup.find_all('div', {'data-hook': 'review'})
print(len(data_tg))
all_stars = []
all_rev = []


def scrape(data_tg):
    for data in data_tg:
        try:
            stars = data.find('i', {'data-hook': 'cmps-review-star-rating'})  # cmps for .com
            star = float(stars.text.strip().split(' ')[0])
            all_stars.append(star)
        except:
            stars = 0.0
            all_stars.append(stars)
        try:
            review = data.find('span', {'data-hook': 'review-title'})
            rev = review.text.strip()
            all_rev.append(rev)

        except:
            review = 'No reviews'
            all_rev.append(review)


def to_dataframe(data):
    df = pandas.Series(data).to_frame('amazon').reset_index()
    df.columns = ['Review', 'Star']
    print('----Data Frame---')
    print(df)
    df.to_csv('Reviews.csv')


scrape(data_tg)
x = dict(zip(all_rev, all_stars))

to_dataframe(x)  # convert to csv and and data frame
