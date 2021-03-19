from collections import deque
from bs4 import BeautifulSoup
# write your code here
import requests
import sys
import os
from colorama import Fore,Style
if __name__ == '__main__':
    downloads_folder = sys.argv[1]
    try:
        os.mkdir(downloads_folder)
    except FileExistsError:
        pass
    tabs_list = deque()
    parsers = ['p', 'a', 'title', 'ul', 'ol', 'li', 'span']

    while True:
        link = input()
        global cur_file
        if link == 'exit':
            exit()

        elif link in tabs_list:
            cur_file = link
            with open(os.path.join(downloads_folder, link), encoding='utf-8') as f:
                text = f.read()
            print(text)


        elif link == 'back':
            try:
                # print('curfile,index', cur_file, tabs_list.index(cur_file))
                link = tabs_list[tabs_list.index(cur_file) - 1]
                print(tabs_list.pop())
                # print('tabs here after bakc',tabs_list)
                with open(os.path.join(downloads_folder, link),encoding='utf-8') as f:
                    text = f.read()
                print(text)
            except:
                print('Cannot go back')


        else:
            try:
                if not link.startswith('http'):
                    link = 'http://' + link
                    print('link here', link)
                text = (requests.get(link))
                soup = BeautifulSoup(text.content, 'html.parser')


                def to_for(soup):
                    strainers = ['a', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'li', 'title']
                    for script in soup(["script", "style"]):
                        script.extract()
                    x = soup.find_all(strainers)
                    p = ''
                    for i in x:
                        line = i.get_text().strip()
                        if i.name == 'a':
                            line = Fore.BLUE + line + '\n'
                            p += line
                        else:
                            line = Fore.WHITE + line + '\n'
                            p += (line)
                    return p

                if 'www.' in link:
                    file_name = link[:(len(link) - link[::-1].index('.', )) - 1].split('www.')[1]
                else:
                    file_name = link[:(len(link) - link[::-1].index('.', )) - 1].split('//')[1]
                cur_file = file_name
                with open(os.path.join(downloads_folder, file_name), 'w+', encoding='utf-8') as f:
                    f.write(to_for(soup))
                print(to_for(soup))
                tabs_list.append(file_name)
            except:
                print('error in extracting data')

        # else:
        #     print('error: Enter valid link')
