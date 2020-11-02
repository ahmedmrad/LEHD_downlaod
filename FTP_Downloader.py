'''
ftp DOWNLOADER
Create an interface that will allow smouth downlowding
Make it an interface
#!/apps/anaconda3-4.3.0/bin/python
#!/apps/anaconda-4.2.0/bin/python

if element is not existing flag it and store it in order to eliminate it
'''
#url_link = 'https://lehd.ces.census.gov/data/lodes/LODES7'

import sys
import os
import os.path
import requests
from bs4 import BeautifulSoup
import mechanicalsoup as ms

os.chdir(os.getcwd())
browser = ms.StatefulBrowser()


def go_to_next(url, element):
    browser = ms.StatefulBrowser()
    browser.open(url)
    browser.follow_link(element)
    return browser.get_url()


def get_href(url, number_elemenent_delete):
    url_soup = requests.get(url).text
    soup = BeautifulSoup(url_soup, 'html.parser')
    my_list = []
    for link in soup.find_all('a'):
        my_list.append(link.get('href'))
    del my_list[0:number_elemenent_delete]
    return my_list


def get_links_toDownload(url):
    next_page = []
    last_page = []
    Download = []
    state_list = get_href(url, 9)
    for state in state_list:
        next_page.append(go_to_next(url, state))
    for page in next_page:
        try:
            last_page.append(go_to_next(page, 'wac/'))
        except ms.LinkNotFoundError:
            continue
    for page_toDownload in last_page:
        Download.append(get_href(page_toDownload, 5))
    return Download, last_page


def main():
    '''
    url_link = 'https://lehd.ces.census.gov/data/lodes/LODES7'
    Check the link because it might have changed
    '''
    input_url = sys.argv[1]
    print(input_url)
    (Download, last_page) = get_links_toDownload(input_url)
    for x in range(len(last_page)):
        for y in range(len(Download[x])):
            file_to_download = last_page[x] + Download[x][y]
            filename = Download[x][y]
            print(file_to_download)
            print(filename)
            r = requests.get(file_to_download)
            with open(filename, 'wb') as f:
                f.write(r.content)


if __name__ == '__main__':
    main()
