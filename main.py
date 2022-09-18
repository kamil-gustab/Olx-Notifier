import certifi                          # certificate issue fix: https://stackoverflow.com/questions/52805115/certificate-verify-failed-unable-to-get-local-issuer-certificate
import re                               # regex; extract substrings
import ssl                              # certificate issue fix: https://stackoverflow.com/questions/52805115/certificate-verify-failed-unable-to-get-local-issuer-certificate
import time                             # delay execution; calculate script's run time
from alive_progress import alive_bar    # progress bar
from bs4 import BeautifulSoup           # BeautifulSoup; parsing HTML
from pprint import pprint               # Nice printing
from urllib.request import urlopen      # open URLs
from urllib import request              # get OLX page source


def scrap_page(url):
    temp_list_of_items = []

    # Adding delay to not block itself
    pause_duration = 3  # seconds to wait
    print("Waiting for", pause_duration, "seconds before opening URL...")
    with alive_bar(pause_duration, bar="circles", spinner="dots_waves") as bar:
        for second in range(0, pause_duration):
            time.sleep(1)
            bar()

    print("Opening page...")
    page = request.urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))
    print("Scraping page...")
    soup = BeautifulSoup(page, features="lxml")  # get URL into BS # *NOTE: v: olx

    counter = 0  # counter to get # of URLs/items
    with alive_bar(bar="classic2", spinner="classic") as bar:  # progress bar
        for link in soup.find_all("a", {"class": "thumb"}):
            temp_list_of_items.append(link.get('href'))
            counter += 1  # counter ++
            bar()  # progress bar ++
    print(f"Successfully added {counter} items to file.")
    return temp_list_of_items


def get_number_of_pages(url_):
    # *NOTE: number of search results pages
    page = urlopen(url_, context=ssl.create_default_context(cafile=certifi.where()))  # fix certificate issue
    soup = BeautifulSoup(page, 'html.parser')  # parse the page
    html_content = soup.body.find('a', attrs={'data-cy': 'page-link-last'})
    num_of_pages = re.search('<span>(.*?)</span>', str(html_content))
    try:  # if there is only 1 page
        num_of_pages = int(num_of_pages.group(1))
    except AttributeError:
        num_of_pages = 1
    print(f'Found {num_of_pages} pages to scrap.')
    return num_of_pages


def remove_dups(list_):
    temp_list = []
    for item in list_:
        end_index = item.find("#")
        if end_index > 0:
            temp_list.append(item[:end_index])
        else:
            temp_list.append(item)
    return set(temp_list)


def get_list_of_ads(url):
    number_of_pages_to_scrap = get_number_of_pages(url)

    page_prefix = '&page='
    page_number = 1  # begin at page=1
    list_of_items = []

    while page_number <= number_of_pages_to_scrap:
        print(f"Page number: {page_number}/{number_of_pages_to_scrap}")
        full_page_url = f"{url}{page_prefix}{page_number}"
        list_of_items.extend(scrap_page(full_page_url))
        page_number += 1  # Go to the next page

    final_set = remove_dups(list_of_items)
    pprint(final_set)
    print(len(final_set))


if __name__ == "__main__":
    # ========== URL to scrape ==========
    page_url = 'https://www.olx.pl/nieruchomosci/stancje-pokoje/krakow/?search%5Border%5D=created_at:desc&search%5Bfilter_float_price:from%5D=600&search%5Bfilter_float_price:to%5D=900'
    # ===================================

    get_list_of_ads(page_url)
