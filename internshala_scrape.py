import urllib3
from bs4 import BeautifulSoup

http = urllib3.PoolManager()
x = int(input('1) category 2) keyword'))
p = input('Job search for:').split()
p = '%20'.join(p)
url = ''
if x == 1:
    url = f'https://internshala.com/internships/work-from-home-{p}-jobs'
elif x == 2:
    url = f'https://internshala.com/internships/keywords-{p}'
else:
    print('No such jobs on the site')
print(url)


def job_search(url):
    r = http.request('GET', url)
    page = r.data.decode()
    page.encode()
    soup = BeautifulSoup(page, 'html.parser')

    salary = soup.find_all('span', class_='stipend')
    company_position = soup.find_all('div', class_='company')
    company_link = soup.find_all('a', class_='view_detail_button')
    print(len(company_position), len(salary))
    for i in range(len(company_position)):
        x = company_position[i].find('a')
        print(x.text, '-->', salary[i].text)
        print('https:/' + company_link[i]['href'])


job_search(url)
