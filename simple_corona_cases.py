import requests
from bs4 import BeautifulSoup
import re

country = input('Country Name: ').lower().split(' ')
country = '-'.join(country)
url = f'https://tradingeconomics.com/{country}/coronavirus-cases'
r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')
tab = soup.find('table', class_='table table-hover')
x = tab.find('a', string=re.compile('\s+Coronavirus Cases\s+'))
y = x.find_next('td').text
print('Total cases reported in the country:', y)

a = tab.find('a', string=re.compile('\s+Coronavirus Deaths\s+'))
b = a.find_next('td').text
print('deaths due to coronavirus:', b)

p = tab.find('a', string=re.compile('\s+Coronavirus Recovered\s+'))
q = p.find_next('td').text
print('patients recovered from corona: ', q)
