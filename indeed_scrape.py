import urllib3
from bs4 import BeautifulSoup

http = urllib3.PoolManager()
position = '+'.join(input('Enter job title or keyword ').split())
position = '%2C'.join(position.split(','))

location = '+'.join(input('Where you are looking for? ').split())
location = '%2C'.join(location.split(','))

start = 0


flag = True

def job_hunt(location, position, start):
    url = f'https://www.indeed.co.in/jobs?q={position}&l={location}&start={start}'
    r = http.request('GET', url)
    page = r.data.decode()
    page.encode()
    soup = BeautifulSoup(page, 'html.parser')
    job = soup.find_all('div', class_='jobsearch-SerpJobCard')
    print('~~~~found', len(job), 'jobs~~~~'.center(5))

    for i in job:
        tit = (i.find('a', class_='jobtitle turnstileLink'))
        if tit is None or tit == '':
            print('No title given')
        else:
            print(tit['title'].strip())
        h = (i.find('span', class_='company'))
        if h is None or h == '':
            print('No company given')
        else:
            print(h.text.strip())
        g = (i.find('span', class_='salaryText'))
        if g is None or g == '':
            print('No salary specifed')
        else:
            print(g.text.strip())
        print('Interested click here ->', f'https://www.indeed.co.in' + tit['href'])
        print()
    if len(job) <= 14:
        print('No more jobs found!')
        global flag
        flag = False


job_hunt(location, position, start)

while flag:
    p = input('Search for more?(y/n)')
    if p.lower() == 'y' or p.lower() == 'yes':
        start += 10
        job_hunt(location, position, start)
    else:
        break
