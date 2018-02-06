#!/usr/bin/python3
'''scraping event details from sfstation.com'''

import requests
import re
from bs4 import BeautifulSoup
from pprint import pprint  # REVISIT: for debugging purpose only.

url = 'https://www.sfstation.com/'
calendar = url + 'calendar/'
page = requests.get(calendar)
soup = BeautifulSoup(page.content, 'html.parser')
events = []  # create a list of dicts where each event attributes are saved

while True:
    # grab all event names and links on the page
    event_names = [name.text for name in soup.find_all('a', class_='url summary')]
    event_links = [link.get('href') for link in soup.find_all('a', class_='url summary')]

    i = 0
    for i in range(len(event_names)):
        event = {}
        event['name'] = event_names[i]
        event['link'] = url + event_links[i]

        # following event link to get additional event info
        event_url = event['link']
        event_page = requests.get(event_url)  # REVISIT: Optimize by using async framework (python-future)
        event_soup = BeautifulSoup(event_page.content, 'html.parser')

        # REVISIT: This only grabs specified event attrs && doesn't take advantage of the flexibility of NoSQL DB
        # REVISIT: How to grab the blurb?
        if event_soup.find('dt', text=re.compile(r'When')):
            date = re.match('^[^(]+', event_soup.find('dd').get_text())
            event['date'] = date.group(0).strip()
        if event_soup.find('span', class_='address'):
            address = event_soup.find('span', class_='address').text
            event['address'] = address
        if event_soup.find('dt', text=re.compile(r'Time')):
            time= event_soup.find('dt', text=re.compile(r'Time')).next_sibling.next_sibling
            event['time'] = time.text
        if event_soup.find('dt', text=re.compile(r'Cost')):
            if event_soup.find('dd', class_='free'):
                event['cost'] = 'free'
            else:
                cost_str= event_soup.find('dt', text=re.compile(r'Cost')).next_sibling.next_sibling
                cost = re.search('\d+', cost_str.text)
                event['cost'] = int(cost.group(0))
        if event_soup.find('dt', text=re.compile(r'Tags')):
            tags = event_soup.find('dt', text=re.compile(r'Tags')).next_sibling.next_sibling
            # save tages as a list of strings
            event['tags'] = tags.text.strip().split(', ')

        events.append(event)
        i += 1

    if soup.select('div#listingPagination > a')[-1].get_text() == 'Next »':
        next_page = url + soup.select('div#listingPagination > a')[-1].get('href')
        page = requests.get(next_page)
        soup = BeautifulSoup(page.content, 'html.parser')
    else:
        break

pprint(events)
