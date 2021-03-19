from selenium import webdriver
from bs4 import BeautifulSoup
import pandas
from urllib.parse import urlparse


class Amazon():
    def __init__(self, product_name, product_id):
        DRIVER_PATH = r'C:\Users\HP\PycharmProjects\mylogger\chromedriver\chromedriver.exe'
        self.url = f'https://www.amazon.com/{product_name}/product-reviews/{product_id}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber=1'  # Learning-Python-Allen-Downey, 9351198146

        options = webdriver.ChromeOptions()
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        self.driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

        self.all_stars = []
        self.all_rev = []

    def scrape(self, soup):
        print('soup here ---',soup)
        data_tg = soup.find_all('div', {'data-hook': 'review'})
        # print(len(data_tg))

        for data in data_tg:
            try:
                stars = data.find('i', {'data-hook': 'cmps-review-star-rating'})  # cmps for .com
                star = float(stars.text.strip().split(' ')[0])
                self.all_stars.append(star)
            except:
                stars = 0.0
                print('n stars found', stars)
                self.all_stars.append(stars)
            try:
                review = data.find('span', {'data-hook': 'review-title'})
                rev = review.text.strip()
                self.all_rev.append(rev)

            except:
                review = 'No reviews'
                self.all_rev.append(review)

    def scrape_all_pages(self):
        while True:
            self.driver.get(self.url)
            content = self.driver.page_source
            page = urlparse(self.url).query.split('&pageNumber=')[1]
            page = page.split('&')[0]
            filename = urlparse(self.url).path.split('/')[1] + str(page) + '.html'
            print(filename)

            with open(filename, 'w', encoding='UTF-8') as f:  # saving the data for reuse without buffer
                cont = f.write(content)

            soup = BeautifulSoup(content, 'html.parser')
            print('scraping next page')
            self.scrape(soup)
            next_page = soup.find('li', class_='a-last')
            try:
                next_page = next_page.a.get('href')
                print(next_page)
                self.url = 'https://www.amazon.com' + next_page
            except:
                print('Finished Scraping')
                self.to_dataframe()  # convert to csv and and data frame
                break

    def to_frame(self, data):  # filters out common reviews
        df = pandas.Series(data).to_frame('amazon').reset_index()
        df.columns = ['Review', 'Star']
        print('----Data Frame---')
        print(df.head)

    def to_dataframe(self):
        print(len(self.all_rev))
        df = pandas.DataFrame({'Reviews': self.all_rev, 'Stars': self.all_stars})
        print(df.head)
        df.to_csv('Reviews.csv')




obj = Amazon('Learning-Python-Allen-Downey', 9351198146)
obj.scrape_all_pages()
