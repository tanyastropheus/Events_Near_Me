#!/usr/bin/python3
'''scraping event details from sfstation.com'''

import requests
import re
import sys
from event_app.db import DB
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from pprint import pprint  # REVISIT: for debugging purpose only.

db = DB('events_today', 'info')
db.delete_index()
db.create_index()
doc_id = 0
url = 'https://www.sfstation.com/{}'
events_calendar = url.format('calendar/bay-area')
page = requests.get(events_calendar)
soup = BeautifulSoup(page.content, 'html.parser')

events = []
while True:
    # grab all event names and links on the page
    event_names = [name.text for name in soup.find_all('a', class_='url summary')]
    event_links = [link.get('href') for link in soup.find_all('a', class_='url summary')]

    for i in range(len(event_names)):
        event = {
            "suggest": []
        }
        event['name'] = event_names[i]
        event_words = event_names[i].split()
        for i in range(len(event_words)):
            event['suggest'].append(' '.join(event_words[i:]))

        print(event['suggest'])
        event['link'] = url.format(event_links[i])

        # following event link to get additional event info
        event_url = event['link']
        event_page = requests.get(event_url)  # REVISIT: Optimize by using async framework (python-future)
        event_soup = BeautifulSoup(event_page.content, 'html.parser')

        # REVISIT: This only grabs specified event attrs && doesn't take advantage of the flexibility of NoSQL DB
        # SOLUTION: include link to the event page
        # REVISIT: How to grab the blurb?
        # REVISIT: What is an event has multiple venues/times/...etc?
        if event_soup.find('dt', text=re.compile(r'When')):
            date = re.match('^[^(]+', event_soup.find('dd').get_text())
            event['date'] = date.group(0).strip()
        if event_soup.select_one('a.businessName'):
            venue = event_soup.select_one('a.businessName').text
            event['venue'] = venue
        if event_soup.find('span', class_='address'):
            address = event_soup.find('span', class_='address').text
            event['address'] = address
        if event_soup.find(id='listingDescription'):
            description = event_soup.find(id='listingDescription').text
            des = description[13:]  # delete 'Description' in the string
            event['description'] = des
        if event_soup.find(id='mainImageOrigLink'):
            image_url = event_soup.find(id='mainImageOrigLink').find_next('a').get('href')
            event['image_url'] = image_url
        if event_soup.find('dt', text=re.compile(r'Time')):
            time= event_soup.find('dt', text=re.compile(r'Time')).find_next('dd').text
            event['time'] = time
        if event_soup.find('dt', text=re.compile(r'Cost')):
            if event_soup.find('dd', class_='free'):
                event['cost'] = 0  # for later price range query comparision
            else:
                cost_str= event_soup.find('dt', text=re.compile(r'Cost')).find_next('dd').text
                cost = re.search('\d+', cost_str)
                event['cost'] = int(cost.group(0))
        elif event_soup.find('dt', text=re.compile(r'Cost')) is None:  # cost is not listed
            event['cost'] = -1  # will translate to 'check event link'
        if event_soup.find('dt', text=re.compile(r'Tags')):
            tags = event_soup.find('dt', text=re.compile(r'Tags')).find_next('dd').text
            # save tages as a list of strings
            event['tags'] = tags.strip().split(', ')

        # TESTING: storing proper events
        pprint(event)
        events.append(event)

        db.store_doc(doc_id, event)
        geo = db.addr_to_geo(doc_id)
        db.save_geo(doc_id, geo)
        doc_id += 1


    print("list of pages:", soup.select('div#listingPagination > a'))
    print("last one:", soup.select('div#listingPagination > a')[-1])

    if soup.select('div#listingPagination > a')[-1].get_text() == 'Next »':
        print("inside")
        next_page = url.format(soup.select('div#listingPagination > a')[-1].get('href'))
        print("next page url:", next_page)
        page = requests.get(next_page)
        print("next page:", page)
        soup = BeautifulSoup(page.content, 'html.parser')
    else:
        break

# TESTING:
print(len(events))
