import os
import os.path
import requests
from bs4 import BeautifulSoup
import mechanicalsoup as ms
import shutil


def go_to_next(url, element):
    '''Extract urls of next pages

    :param url: url link
    :type url: str
    :param element: element to be extracted
    :type element:
    :returns browser.get_url(): extracted url with mechanical soup
    :rtype browser.get_url(): str
    '''
    browser = ms.StatefulBrowser()
    browser.open(url)
    browser.follow_link(element)
    return browser.get_url()


def get_href(url, number_elemenent_delete):
    '''Extract href from website

    :param url: url link
    :type url: str
    :param number_elements_delete: number of empty folders
    :type number_elements_delete: int
    :returns my_list: list of href links
    :rtype my_list: list
    '''
    url_soup = requests.get(url).text
    soup = BeautifulSoup(url_soup, 'html.parser')
    my_list = []
    for link in soup.find_all('a'):
        my_list.append(link.get('href'))
    del my_list[0:number_elemenent_delete]
    return my_list


def get_links_toDownload(url):
    """Extract url links to be downloaded from the main url link

    :param url: url link
    :type url: str
    ...
    :raises LinkNotFoundError: link not working or not found
    ...
    :returns download: list url of all the csv files
    :rtype downlaod: list
    :returns last_page: urls of the folder where the csv files are located
    :rtype last_page: list
    """
    next_page = []
    last_page = []
    download = []
    # the first 10 href are not state folders. check in the future
    state_list = get_href(url, 10)
    print(state_list)
    for state in state_list:
        next_page.append(go_to_next(url, state))
    for page in next_page:
        try:
            print(page)
            last_page.append(go_to_next(page, 'wac/'))
        except ms.LinkNotFoundError:
            continue
    for page_to_download in last_page:
        print(page_to_download)
        download.append(get_href(page_to_download, 5))
    return download, last_page


def main():
    current_path = os.getcwd()
    all_lehd_files_path = current_path + '/lehd_files'
    if os.path.exists(all_lehd_files_path):
        shutil.rmtree(all_lehd_files_path)
    os.makedirs(all_lehd_files_path)
    os.chdir(all_lehd_files_path)
    (download, last_page) = get_links_toDownload(
        'https://lehd.ces.census.gov/data/lodes/LODES7')
    for x in range(len(last_page)):
        for y in range(len(download[x])):
            file_to_download = last_page[x] + download[x][y]
            filename = download[x][y]
            r = requests.get(file_to_download)
            with open(filename, 'wb') as f:
                f.write(r.content)


if __name__ == '__main__':
    main()
