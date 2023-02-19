import argparse                         # Parse arguments
import certifi                          # Certificate issue fix: https://stackoverflow.com/questions/52805115/certificate-verify-failed-unable-to-get-local-issuer-certificate
import email_notificator                # File import
import os
import re                               # Regex; extract substrings
import ssl                              # Certificate issue fix: https://stackoverflow.com/questions/52805115/certificate-verify-failed-unable-to-get-local-issuer-certificate
import telegram_send                    # Telegram message sending library
import time                             # Delay execution
from alive_progress import alive_bar    # Progress bar
from bs4 import BeautifulSoup           # BeautifulSoup; parsing HTML
from urllib.request import urlopen      # Open URLs
from urllib import request              # Get OLX page source


def scrap_page(url):
    temp_list_of_items = []

    # Adding delay to not block itself
    pause_duration = 3  # seconds to wait
    print(f"Waiting for {pause_duration} seconds before opening URL...")
    with alive_bar(pause_duration, bar="circles", spinner="dots_waves") as bar:
        for second in range(0, pause_duration):
            time.sleep(1)
            bar()

    print("Opening page...")
    page = request.urlopen(url,
                           context=ssl.create_default_context(cafile=certifi.where()))
    print("Scraping page...")
    soup = BeautifulSoup(page, features="lxml")

    # When looking for work - links are in different classes
    if "olx.pl/praca" not in url:
        target_class = "thumb"
    else:
        target_class = "marginright5"

    counter = 0  # counter to get # of URLs/items
    with alive_bar(bar="classic2", spinner="classic") as bar:  # progress bar
        for link in soup.find_all("a", {"class": target_class}):
            temp_list_of_items.append(link.get("href"))
            counter += 1  # counter ++
            bar()  # progress bar ++
    print(f"Found {counter} items on page.")
    return temp_list_of_items


def get_number_of_pages(url_):
    # *NOTE: number of search results pages
    page = urlopen(url_, context=ssl.create_default_context(cafile=certifi.where()))  # fix certificate issue
    soup = BeautifulSoup(page, "html.parser")  # parse the page
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
        # temp_item = temp_item.split("?")[0]
        temp_list.append(item.split("#")[0])
    return set(temp_list)


def get_list_of_ads(url):
    number_of_pages_to_scrap = get_number_of_pages(url)

    # When looking for work - links for pages work differently
    if "olx.pl/praca" not in url:
        page_prefix = "&page="
    else:
        page_prefix = "?page="

    page_number = 1
    list_of_items = []

    while page_number <= number_of_pages_to_scrap:
        print(f"Page number: {page_number}/{number_of_pages_to_scrap}")
        full_page_url = f"{url}{page_prefix}{page_number}"
        list_of_items.extend(scrap_page(full_page_url))
        page_number += 1  # Go to the next page

    final_set = remove_dups(list_of_items)
    print(f"Finaly found {len(final_set)} records.")
    return final_set


def write_to_file(data):
    with open("previous_results.txt", "a") as file:
        if len(data) == 1:
            new_data = f"\n{str(data)[2:-2]}"
        else:
            new_data = str(data)[2:-2].replace("', '", "\n")
        file.write(new_data)


def check_data(data):
    global first_run
    try:
        with open("previous_results.txt", "r") as file:
            file_content = file.read()
    except FileNotFoundError:
        print("First run, creating file...")
        cwd = os.getcwd()
        os.system(f"touch {cwd}/previous_results.txt")
        first_run = True
        file_content = ""

    found_ads = []
    for item in data:
        if item not in file_content:
            found_ads.append(item)

    print(f"Found {len(found_ads)} new ad(s)"
          f" - compared to the previous search:\n")
    return found_ads


def notify_mail(data):
    print("Sending notification(s) through Mail!")
    email_notificator.send_mail(data)


def notify_telegram(data):
    print("Sending notification(s) through Telegram!")
    telegram_send.send(messages=data)


def format_url(url):
    if url[-1] == "/":
        url = url[:-1]
    return url.replace("olx.pl/d/", "olx.pl/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, required=False)
    parser.add_argument('--notify', type=str, required=True,
                        choices=['mail', 'no-notify', 'telegram'])
    args = parser.parse_args()
    first_run = False

    if args.url:
        given_url = args.url
    else:
        print("You didn't provide url as parameter, taking default from file code...")
        # ========== URL to scrape if nothing given in parameter ==========
        given_url = 'https://www.olx.pl/nieruchomosci/stancje-pokoje/krakow/?search%5Border%5D=created_at:desc&search%5Bfilter_float_price:from%5D=600&search%5Bfilter_float_price:to%5D=900'
        # =================================================================

    page_url = format_url(given_url)
    ads_list = get_list_of_ads(page_url)
    new_ads = check_data(ads_list)
    if new_ads:
        write_to_file(new_ads)
        if first_run:
            print("It's first run, not sending any notifications.")
        else:
            print(*new_ads, sep="\n")
            if args.notify == "telegram":
                notify_telegram(new_ads)
            elif args.notify == "mail":
                notify_mail(new_ads)
            else:
                print("You've chosen --notify no-notify - not sending any notify.")
