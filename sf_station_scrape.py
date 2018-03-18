#!/usr/bin/python3
'''scraping event details from sfstation.com'''

import requests
import re
import sys
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from pprint import pprint  # REVISIT: for debugging purpose only.

# connect to ES server
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
doc_id = 0

url = 'https://www.sfstation.com/'
calendar = url + 'calendar/'
page = requests.get(calendar)
soup = BeautifulSoup(page.content, 'html.parser')

# TESTING: have the same number of event entries as stored in Elasticsearch
events = []

'''
# TESTING: delete past indexes to start anew
es.indices.delete(index='events')
sys.exit()
'''
while True:
    # grab all event names and links on the page
    event_names = [name.text for name in soup.find_all('a', class_='url summary')]
    event_links = [link.get('href') for link in soup.find_all('a', class_='url summary')]

    for i in range(len(event_names)):
        event = {}
        event['name'] = event_names[i]
        event['link'] = url + event_links[i]

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
        if event_soup.select('.businessName'):
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
        if event_soup.find('dt', text=re.compile(r'Tags')):
            tags = event_soup.find('dt', text=re.compile(r'Tags')).find_next('dd').text
            # save tages as a list of strings
            event['tags'] = tags.strip().split(', ')

        # TESTING: storing proper events
        pprint(event)
        events.append(event)

        # store event data in ES
        es.index(index='events', doc_type='info', id=doc_id, body=event)
        doc_id += 1

    if soup.select('div#listingPagination > a')[-1].get_text() == 'Next »':
        next_page = url + soup.select('div#listingPagination > a')[-1].get('href')
        page = requests.get(next_page)
        soup = BeautifulSoup(page.content, 'html.parser')
    else:
        break

# TESTING:
print(len(events))
